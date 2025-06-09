<script setup>
// --- Імпорти стандартних API Vue та Nuxt/Vue Router ---
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'
import { useRouter } from '#app'
import treeDataRaw from '@/data/data.json'

// --- Приймаємо treeID як пропс (ідентифікатор потрібної гілки) ---
const props = defineProps({ treeID: { type: String, default: "1" } })

// --- Константи для розмітки вузлів та відступів ---
const fixedRectW = 170           // Ширина прямокутника особи
const rectH = 88                 // Висота прямокутника особи
const vertGap = 140              // Вертикальний відступ між поколіннями
const pairGap = 60               // Відстань між подружжям
const minChildGap = 60           // Мінімальний відступ між дітьми

// --- SVG: ширина вікна (адаптивність) та фіксована висота ---
const svgWidth = ref(typeof window !== 'undefined' ? window.innerWidth : 3000)
const svgHeight = 1600           // Вистачає на велике дерево

// --- Адаптація ширини SVG при зміні розміру вікна ---
const updateSvgWidth = () => { svgWidth.value = window.innerWidth }
onMounted(() => {
  svgWidth.value = window.innerWidth
  window.addEventListener('resize', updateSvgWidth)
})
onBeforeUnmount(() => { window.removeEventListener('resize', updateSvgWidth) })

// --- Основна гілка дерева за ID (реактивно) ---
const mainBranch = computed(() => treeDataRaw.find(branch => branch.treeID === props.treeID))
const familyTree = computed(() => mainBranch.value?.treeData ?? {})
const treeTitle = computed(() => mainBranch.value?.treeBranch ?? "Родинне дерево")

// --- Ініціалізація роутера для переходів між гілками ---
const router = useRouter()

// --- Дебаг: спостерігаємо за змінами treeID (можна вимкнути) ---
watch(() => props.treeID, (val) => {
  console.log("treeID змінився, новий:", val)
})

/**
 * Рекурсивна функція для розрахунку позицій вузлів і побудови всієї структури.
 * @param person - основна особа (наприклад, чоловік)
 * @param partner - партнер особи (наприклад, дружина)
 * @param x, y - координати центру вузла
 * @return структура з позиціями, лінками, межами піддерева
 */
function layoutPerson(person, partner, x, y) {
  const hasPartner = partner && partner.name
  let nodes = []

  // --- Ширина прямокутників особи і партнера ---
  const personRectW = fixedRectW
  const partnerRectW = hasPartner ? fixedRectW : 0
  const localPairGap = hasPartner ? (personRectW / 2 + partnerRectW / 2 + pairGap) : 0

  // --- Масив дітей, якщо вони є ---
  const children = Array.isArray(person.children) ? person.children : []
  let childResults = []

  // --- Рекурсія по дітях (у кожної дитини теж може бути партнер) ---
  children.forEach((child, i) => {
    const childPartner = child.wife || child.husband || null
    const res = layoutPerson(child, childPartner, 0, y + vertGap)
    childResults.push(res)
  })

  // --- Обчислюємо ширину піддерева по дітях ---
  let maxChildBlockWidth = fixedRectW
  if (childResults.length) {
    maxChildBlockWidth = Math.max(...childResults.map(res =>
        (res.selfNode ? fixedRectW : 0) + (res.partnerRectW ?? 0) + (res.hasPartner ? pairGap : 0)
    ))
    if (maxChildBlockWidth < fixedRectW) maxChildBlockWidth = fixedRectW
  }

  // --- Ширина кожного піддерева дитини ---
  let subtreeWidths = childResults.map(res =>
      Math.max(
          maxChildBlockWidth,
          res.widthSubtree
      )
  )

  // --- Загальна ширина блоку вузла (основний вузол + партнер, якщо є) ---
  let widthSelfBlock = hasPartner ? (personRectW + partnerRectW + localPairGap) : personRectW
  let widthChildren = subtreeWidths.length
      ? subtreeWidths.reduce((a, b) => a + b, 0) + (subtreeWidths.length - 1) * minChildGap
      : 0
  let widthSubtree = Math.max(widthSelfBlock, widthChildren)

  // --- Обчислюємо x-координати дітей (платформа розподіляє їх по ширині) ---
  let firstChildX;
  if (childResults.length === 1) {
    const onlyChild = childResults[0];
    if (onlyChild.hasPartner) {
      // Якщо у дитини теж є партнер — платформа більша
      const platformWidth = fixedRectW + onlyChild.partnerRectW + pairGap + 60;
      firstChildX = x - platformWidth / 2 + fixedRectW / 2;
    } else {
      firstChildX = x - fixedRectW / 2;
    }
  } else {
    firstChildX = x - widthChildren / 2;
  }
  let curX = firstChildX;
  childResults.forEach((res, i) => {
    const width = subtreeWidths[i]
    const nodeWidth = (res.selfNode ? fixedRectW : 0) + (res.partnerRectW ?? 0) + (res.hasPartner ? pairGap : 0)
    const newNodeCenterX = curX + nodeWidth / 2
    const dx = newNodeCenterX - res.selfNode.x
    // --- Зміщуємо всю підгілку вправо/вліво, щоб була гарна платформа ---
    res.nodes.forEach(n => n.x += dx)
    res.links.forEach(l => {
      if (l.x !== undefined) l.x += dx
      if (l.x1 !== undefined) l.x1 += dx
      if (l.x2 !== undefined) l.x2 += dx
    })
    res.selfNode.x += dx
    res.minX += dx
    res.maxX += dx
    curX += width + minChildGap
  })

  // --- Границі піддерева (для вирівнювання) ---
  let minX, maxX
  if (childResults.length > 0) {
    minX = Math.min(...childResults.map(r => r.minX))
    maxX = Math.max(...childResults.map(r => r.maxX))
  } else if (hasPartner) {
    minX = x - localPairGap / 2 - personRectW / 2
    maxX = x + localPairGap / 2 + partnerRectW / 2
  } else {
    minX = x - personRectW / 2
    maxX = x + personRectW / 2
  }

  // --- Основний вузол і партнер (якщо є) ---
  const mainPersonX = hasPartner ? x - localPairGap / 2 : x
  nodes.push({
    ...person,
    x: mainPersonX,
    y,
    id: person.id,
    isPerson: true,
    rectW: fixedRectW,
    treeRef: person.treeRef // для переходу у гілку
  })
  if (hasPartner) {
    nodes.push({
      ...partner,
      x: x + localPairGap / 2,
      y,
      id: partner.id,
      isPerson: true,
      rectW: fixedRectW,
      treeRef: partner.treeRef // для переходу у гілку
    })
    nodes.push({
      id: `${person.id}_${partner.id}_marriage`,
      isMarriage: true,
      x: x,
      y: y
    })
  }

  // --- Лінки (ребра) для дерева: шлюби, зв'язки до дітей і платформи ---
  let links = []
  if (hasPartner) {
    // Від батьків до шлюбу
    links.push({ from: person.id, to: `${person.id}_${partner.id}_marriage` })
    links.push({ from: partner.id, to: `${person.id}_${partner.id}_marriage` })
  }

  // --- Побудова "платформи" для дітей (горизонтальна лінія під шлюбом/батьком) ---
  const yPlat = y + vertGap - vertGap / 2
  if (childResults.length) {
    const childNodes = childResults.map(res => res.selfNode)
    const onlyChild = childResults[0];
    if (hasPartner) {
      // Шлюб є
      if (childNodes.length === 1 && onlyChild.hasPartner) {
        // Якщо одна дитина і у неї теж партнер — платформа ширша
        links.push({
          from: `${person.id}_${partner.id}_marriage`,
          to: null,
          x: x,
          y1: y,
          y2: yPlat,
          direction: "marriageToPlatform"
        });
        const platformWidth = fixedRectW + onlyChild.partnerRectW + pairGap + 60;
        const platMinX = onlyChild.selfNode.x - (platformWidth / 2) + fixedRectW / 2;
        const platMaxX = onlyChild.selfNode.x + (platformWidth / 2) - fixedRectW / 2;
        links.push({
          from: null,
          to: null,
          x1: platMinX,
          x2: platMaxX,
          y: yPlat,
          direction: "platform"
        });
        links.push({
          from: null,
          to: onlyChild.selfNode.id,
          x: onlyChild.selfNode.x,
          y1: yPlat,
          y2: onlyChild.selfNode.y,
          direction: "platformToChild"
        });
      } else if (childNodes.length === 1) {
        // Шлюб → одна дитина
        links.push({
          from: `${person.id}_${partner.id}_marriage`,
          to: childNodes[0].id,
          direction: "marriageToChild"
        });
      } else {
        // Кілька дітей — платформа
        links.push({
          from: `${person.id}_${partner.id}_marriage`,
          to: null,
          x: x,
          y1: y,
          y2: yPlat,
          direction: "marriageToPlatform"
        });
        const platMinX = childNodes[0].x
        const platMaxX = childNodes[childNodes.length - 1].x
        links.push({
          from: null,
          to: null,
          x1: platMinX,
          x2: platMaxX,
          y: yPlat,
          direction: "platform"
        });
        childNodes.forEach(child => {
          links.push({
            from: null,
            to: child.id,
            x: child.x,
            y1: yPlat,
            y2: child.y,
            direction: "platformToChild"
          });
        });
      }
    } else {
      // Без шлюбу — "соло" вузол
      if (childNodes.length === 1 && onlyChild.hasPartner) {
        // Одна дитина з партнером — платформа ширша
        links.push({
          from: person.id,
          to: null,
          x: x,
          y1: y,
          y2: yPlat,
          direction: "marriageToPlatform"
        });
        const platformWidth = fixedRectW + onlyChild.partnerRectW + pairGap + 60;
        const platMinX = onlyChild.selfNode.x - (platformWidth / 2) + fixedRectW / 2;
        const platMaxX = onlyChild.selfNode.x + (platformWidth / 2) - fixedRectW / 2;
        links.push({
          from: null,
          to: null,
          x1: platMinX,
          x2: platMaxX,
          y: yPlat,
          direction: "platform"
        });
        links.push({
          from: null,
          to: onlyChild.selfNode.id,
          x: onlyChild.selfNode.x,
          y1: yPlat,
          y2: onlyChild.selfNode.y,
          direction: "platformToChild"
        });
      } else if (childNodes.length === 1) {
        // Соло вузол → одна дитина
        links.push({
          from: person.id,
          to: childNodes[0].id,
          direction: "personToChild"
        });
      } else {
        // Кілька дітей — платформа
        links.push({
          from: person.id,
          to: null,
          x: x,
          y1: y,
          y2: yPlat,
          direction: "marriageToPlatform"
        });
        const platMinX = childNodes[0].x
        const platMaxX = childNodes[childNodes.length - 1].x
        links.push({
          from: null,
          to: null,
          x1: platMinX,
          x2: platMaxX,
          y: yPlat,
          direction: "platform"
        });
        childNodes.forEach(child => {
          links.push({
            from: null,
            to: child.id,
            x: child.x,
            y1: yPlat,
            y2: child.y,
            direction: "platformToChild"
          });
        });
      }
    }
  }

  // --- Додаємо вузли і лінки дочірніх піддерев ---
  childResults.forEach(res => {
    nodes = nodes.concat(res.nodes)
    links = links.concat(res.links)
  })

  // --- Повертаємо структуру для цього вузла і всієї його підгілки ---
  return {
    selfNode: {
      id: person.id,
      x: mainPersonX,
      y: y,
      surname: person.surname,
      name: person.name,
      patronymic: person.patronymic,
      gender: person.gender,
      rectW: fixedRectW,
      treeRef: person.treeRef
    },
    partnerRectW: hasPartner ? fixedRectW : 0,
    hasPartner,
    nodes,
    links,
    minX,
    maxX,
    widthSubtree
  }
}

// --- Обчислення повного layout для дерева (reactive) ---
const treeLayout = computed(() => {
  // Вибираємо партнера основної особи гілки
  const partner = familyTree.value.wife || familyTree.value.husband || null
  return layoutPerson(familyTree.value, partner, svgWidth.value / 2, 180)
})

// --- Всі вузли і лінки для SVG (reactive) ---
const allNodes = computed(() => treeLayout.value.nodes)
const allLinks = computed(() => treeLayout.value.links)

// --- Підтримка drag/pan та zoom (ViewBox SVG) ---
const svgRef = ref(null)
const viewBox = ref({ x: 0, y: 0, width: svgWidth.value, height: svgHeight })
let isPanning = false
let startPoint = { x: 0, y: 0 }
let startViewBox = { x: 0, y: 0, width: svgWidth.value, height: svgHeight }

// --- Масштабування колеса миші (zoom) ---
function onWheel(e) {
  const scale = e.deltaY < 0 ? 0.9 : 1.1
  const mx = e.offsetX
  const my = e.offsetY
  const { x, y, width: w, height: h } = viewBox.value
  const newW = w * scale
  const newH = h * scale
  const dx = ((mx / svgWidth.value) * (w - newW))
  const dy = ((my / svgHeight) * (h - newH))
  viewBox.value = {
    x: x + dx,
    y: y + dy,
    width: newW,
    height: newH
  }
}
// --- Початок переміщення (pan) ---
function onMouseDown(e) {
  isPanning = true
  startPoint = { x: e.clientX, y: e.clientY }
  startViewBox = { ...viewBox.value }
}
// --- Переміщення (pan) ---
function onMouseMove(e) {
  if (!isPanning) return
  const dx = ((e.clientX - startPoint.x) * viewBox.value.width) / svgWidth.value
  const dy = ((e.clientY - startPoint.y) * viewBox.value.height) / svgHeight
  viewBox.value = {
    ...viewBox.value,
    x: startViewBox.x - dx,
    y: startViewBox.y - dy
  }
}
// --- Кінець переміщення (pan) ---
function onMouseUp() { isPanning = false }

// --- Перехід у гілку при натисканні на вузол з treeRef ---
function onPersonClick(node) {
  if (node.treeRef) {
    router.push(`/branch/${node.treeRef}`)
  }
}
</script>

<template>
  <v-app>
    <v-container fluid>
      <!-- Заголовок Material UI -->
      <v-row justify="center">
        <v-col cols="auto">
          <v-sheet elevation="3" class="pa-6 mb-4" rounded="xl">
            <v-typography
                variant="h2"
                align="center"
                class="font-weight-bold"
            >
              {{ treeTitle }}
            </v-typography>
          </v-sheet>
        </v-col>
      </v-row>
      <!-- Карта для SVG дерева -->
      <v-row justify="center">
        <v-col cols="12">
          <v-card
              elevation="8"
              class="pa-2 mb-4"
              rounded="2xl"
              style="background: #fff; max-height: 85vh; overflow: hidden;"
          >
            <!-- SVG дерево (з твого коду) -->
            <svg
                ref="svgRef"
                :viewBox="`${viewBox.x} ${viewBox.y} ${viewBox.width} ${viewBox.height}`"
                :width="svgWidth"
                height="75vh"
                style="background: #fff; border-radius: 18px; box-shadow:0 3px 12px #0001; cursor:grab; user-select: none;"
                @mousedown="onMouseDown"
                @mousemove="onMouseMove"
                @mouseup="onMouseUp"
                @mouseleave="onMouseUp"
                @wheel.prevent="onWheel"
            >
              <defs>
                <!-- Градієнти та патерни для вузлів -->
                <linearGradient id="maleGrad" x1="0" y1="0" x2="1" y2="1">
                  <stop offset="0%" stop-color="#3ddcff" />
                  <stop offset="100%" stop-color="#2572d3" />
                </linearGradient>
                <linearGradient id="femaleGrad" x1="0" y1="0" x2="1" y2="1">
                  <stop offset="0%" stop-color="#ffadc2" />
                  <stop offset="100%" stop-color="#e864a7" />
                </linearGradient>
                <pattern id="malePattern" patternUnits="userSpaceOnUse" width="40" height="40">
                  <rect width="40" height="40" fill="url(#maleGrad)"/>
                  <path d="M0 28 Q 10 16, 20 28 T 40 28" stroke="#fff" stroke-width="2" fill="none" opacity="0.14"/>
                  <path d="M0 36 Q 10 28, 20 36 T 40 36" stroke="#fff" stroke-width="2" fill="none" opacity="0.08"/>
                </pattern>
                <pattern id="femalePattern" patternUnits="userSpaceOnUse" width="40" height="40">
                  <rect width="40" height="40" fill="url(#femaleGrad)"/>
                  <path d="M0 28 Q 10 16, 20 28 T 40 28" stroke="#fff" stroke-width="2" fill="none" opacity="0.13"/>
                  <path d="M0 36 Q 10 28, 20 36 T 40 36" stroke="#fff" stroke-width="2" fill="none" opacity="0.07"/>
                </pattern>
              </defs>
              <!-- Лінії (зв'язки) -->
              <g>
                <template v-for="(link, idx) in allLinks" :key="'link-'+idx">
                  <!-- Всі варіанти зв'язків, платформа, шлюб, батьки, діти -->
                  <line
                      v-if="link.direction === 'marriageToChild'"
                      :x1="allNodes.find(n=>n.id===link.from)?.x"
                      :y1="allNodes.find(n=>n.id===link.from)?.y"
                      :x2="allNodes.find(n=>n.id===link.to)?.x"
                      :y2="allNodes.find(n=>n.id===link.to)?.y"
                      stroke="#bbb" stroke-width="3" opacity="0.6"
                  />
                  <line
                      v-else-if="link.direction === 'personToChild'"
                      :x1="allNodes.find(n=>n.id===link.from)?.x"
                      :y1="allNodes.find(n=>n.id===link.from)?.y"
                      :x2="allNodes.find(n=>n.id===link.to)?.x"
                      :y2="allNodes.find(n=>n.id===link.to)?.y"
                      stroke="#bbb" stroke-width="3" opacity="0.6"
                  />
                  <line
                      v-else-if="link.direction === 'marriageToPlatform'"
                      :x1="link.x"
                      :y1="link.y1"
                      :x2="link.x"
                      :y2="link.y2"
                      stroke="#bbb" stroke-width="3" opacity="0.6"
                  />
                  <line
                      v-else-if="link.direction === 'platform' && Math.abs(link.x2 - link.x1) > 10"
                      :x1="link.x1"
                      :y1="link.y"
                      :x2="link.x2"
                      :y2="link.y"
                      stroke="#333" stroke-width="3" opacity="0.9"
                  />
                  <line
                      v-else-if="link.direction === 'platformToChild'"
                      :x1="link.x"
                      :y1="link.y1"
                      :x2="link.x"
                      :y2="link.y2"
                      stroke="#444"
                      stroke-width="3"
                      opacity="0.7"
                  />
                  <line
                      v-else
                      :x1="allNodes.find(n=>n.id===link.from)?.x"
                      :y1="allNodes.find(n=>n.id===link.from)?.y"
                      :x2="allNodes.find(n=>n.id===link.to)?.x"
                      :y2="allNodes.find(n=>n.id===link.to)?.y"
                      stroke="#ccc"
                      stroke-width="3"
                      opacity="0.7"
                  />
                </template>
              </g>
              <!-- Вузли -->
              <g>
                <template v-for="node in allNodes" :key="'node-'+node.id">
                  <!-- Прямокутник вузла (особа або партнер), з клікабельністю якщо є гілка -->
                  <rect
                      v-if="!node.isMarriage"
                      :x="node.x - fixedRectW / 2"
                      :y="node.y - rectH / 2"
                      :width="fixedRectW"
                      :height="rectH"
                      :rx="24"
                      :fill="node.gender === 'male' ? 'url(#malePattern)' : 'url(#femalePattern)'"
                      :stroke="node.treeRef ? '#009b36' : '#222'"
                      :stroke-width="node.treeRef ? 4 : 2"
                      @click="onPersonClick(node)"
                      :style="{
                      cursor: node.treeRef ? 'pointer' : 'default',
                      filter: 'drop-shadow(0 6px 32px #009b3633) blur(0.4px) saturate(1.15)',
                      opacity: 0.93,
                      transition: 'filter 0.3s, stroke 0.3s, opacity 0.3s'
                    }"
                      :onmouseover="event => event.target.style.filter='drop-shadow(0 16px 48px #009b36cc) blur(2.2px)'"
                      :onmouseleave="event => event.target.style.filter='drop-shadow(0 6px 32px #009b3633) blur(0.4px) saturate(1.15)'"
                      :title="node.treeRef ? 'Перейти у гілку' : ''"
                  />
                  <!-- Прізвище -->
                  <text
                      v-if="!node.isMarriage"
                      :x="node.x"
                      :y="node.y - 20"
                      text-anchor="middle"
                      font-size="18"
                      font-family="Inter, Arial, sans-serif"
                      font-weight="bold"
                      fill="#111"
                      style="pointer-events:none"
                  >{{ node.surname }}</text>
                  <!-- Ім'я -->
                  <text
                      v-if="!node.isMarriage"
                      :x="node.x"
                      :y="node.y"
                      text-anchor="middle"
                      font-size="17"
                      font-family="Inter, Arial, sans-serif"
                      font-weight="bold"
                      fill="#111"
                      style="pointer-events:none"
                  >{{ node.name }}</text>
                  <!-- По батькові -->
                  <text
                      v-if="!node.isMarriage"
                      :x="node.x"
                      :y="node.y + 16"
                      text-anchor="middle"
                      font-size="17"
                      font-family="Inter, Arial, sans-serif"
                      font-weight="bold"
                      fill="#111"
                      style="pointer-events:none"
                  >{{ node.patronymic }}</text>
                  <!-- Дати народження/смерті -->
                  <text
                      v-if="!node.isMarriage && node.birthDate"
                      :x="node.x"
                      :y="node.y + 32"
                      text-anchor="middle"
                      font-size="13"
                      font-family="Inter, Arial, sans-serif"
                      font-weight="bold"
                      fill="#111"
                      style="pointer-events:none"
                  >{{ node.birthDate }} {{node.deathDate }}</text>
                  <!-- Вузол шлюбу (коло) -->
                  <circle
                      v-if="node.isMarriage"
                      :cx="node.x"
                      :cy="node.y"
                      r="15"
                      fill="#fff7"
                      stroke="#ccc"
                      stroke-width="2"
                      opacity="0.8"
                      style="backdrop-filter: blur(6px);"
                  />
                </template>
              </g>
            </svg>
            <!-- Кнопка повернення -->
            <div v-if="props.treeID !== '1'" style="text-align:center; margin-top:32px; margin-bottom:16px;">
              <v-btn
                  color="primary"
                  prepend-icon="mdi-arrow-left"
                  elevation="4"
                  class="text-h6"
                  rounded="xl"
                  @click="router.push('/tree')"
              >
                Повернутись до основної гілки
              </v-btn>
            </div>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </v-app>
</template>

