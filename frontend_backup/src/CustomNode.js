import React from "react";

const CustomNode = ({ nodeDatum, toggleNode }) => {
    const { name, attributes } = nodeDatum;
    const gender = attributes?.gender;
    const birth = attributes?.birth;
    const death = attributes?.death;
    const isSpouse = attributes?.isSpouse;
    const spouseOf = attributes?.spouseOf;

    const bgColor = gender === "male" ? "#1E90FF" : gender === "female" ? "#FF69B4" : "#ccc";

    // Визначаємо зміщення: якщо spouse — зсуваємо правіше
    const offsetX = isSpouse ? 100 : 0;

    return (
        <g transform={`translate(${offsetX}, 0)`} onClick={toggleNode}>
            <rect
                width={150}
                height={isSpouse ? 60 : 80}
                x={-75}
                y={-40}
                rx={10}
                fill={bgColor}
                stroke="#000"
                strokeWidth={1}
            />
            <text x={0} y={-10} textAnchor="middle" fill="#fff" fontSize={14}>
                {name}
            </text>
            <text x={0} y={10} textAnchor="middle" fill="#fff" fontSize={11}>
                {`* ${birth} ✝ ${death}`}
            </text>
            {isSpouse && (
                <text x={0} y={28} textAnchor="middle" fill="#fff" fontSize={11}>
                    Подружжя: {spouseOf}
                </text>
            )}
        </g>
    );
};

export default CustomNode;
