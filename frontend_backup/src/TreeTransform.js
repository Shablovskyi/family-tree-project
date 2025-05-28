export const transformTreeData = (person) => {
    const buildNode = (p, isSpouse = false, spouseName = "") => {
        const node = {
            name: p.name,
            attributes: {
                birth: p.birthDate || "—",
                death: p.deathDate || "—",
                gender: p.gender || "—",
            },
            nodeSvgShape: {
                shape: "circle",
                shapeProps: {
                    r: 10,
                    fill: p.gender === "male" ? "#1E90FF" : "#FF69B4",
                    stroke: "#000000",
                },
            },
        };

        if (isSpouse) {
            node.attributes.isSpouse = true;
            node.attributes.spouseOf = spouseName;
        }

        if (p.children && !isSpouse) {
            node.children = p.children.map(transformTreeData);
        }

        return node;
    };

    const spouse = person.wife || person.husband;
    const mainNode = buildNode(person);
    const children = [];

    if (spouse && spouse.name) {
        const spouseNode = buildNode(spouse, true, person.name);
        children.push(spouseNode);
    }

    if (mainNode.children) {
        children.push(...mainNode.children);
    }

    mainNode.children = children;

    return mainNode;
};
