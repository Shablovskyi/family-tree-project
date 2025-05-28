import React, { useRef, useEffect, useState } from "react";
import Tree from "react-d3-tree";
import { transformTreeData } from "./TreeTransform";
import CustomNode from "./CustomNode";

const FamilyTree = ({ treeData, onNavigateToBranch }) => {
    const containerRef = useRef(null);
    const [dimensions, setDimensions] = useState({ width: 0, height: 0 });

    useEffect(() => {
        if (containerRef.current) {
            const { width, height } = containerRef.current.getBoundingClientRect();
            setDimensions({ width, height });
        }
    }, []);

    const handleNodeClick = (nodeData) => {
        if (nodeData.data.eventKey) {
            onNavigateToBranch(nodeData.data.eventKey);
        }
    };

    const transformedData = transformTreeData(treeData, onNavigateToBranch);

    return (
        <div ref={containerRef} style={{ width: "100%", height: "80vh" }}>
            {dimensions.width > 0 && (
                <Tree
                    data={transformedData}
                    translate={{ x: dimensions.width / 2, y: 100 }}
                    orientation="vertical"
                    zoomable
                    collapsible
                    nodeSize={{ x: 220, y: 200 }}
                    separation={{ siblings: 1.2, nonSiblings: 1.8 }}
                    onNodeClick={handleNodeClick}
                    renderCustomNodeElement={(rd3tProps) => <CustomNode {...rd3tProps} />}
                />
            )}
        </div>
    );
};

export default FamilyTree;
