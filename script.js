document.addEventListener('DOMContentLoaded', () => {
    const resultsContainer = document.getElementById('results-container');
    const cyContainer = document.getElementById('cy');
    // ⭐ NLQ SIMULATION LOGIC ⭐
    const nlqInput = document.getElementById('nlq-input');
    const nlqButton = document.getElementById('nlq-button');
    const nlqOutput = document.getElementById('nlq-output');
    const mainContent = document.getElementById('main-dashboard-content');
    
    // --- 1. Dynamic Data File Assignment ---
    const pageName = window.location.pathname.split('/').pop().split('.')[0];
    let dataFile = '';
    let categoryName = '';

    if (pageName === 'index' || pageName === '') {
        dataFile = 'musculoskeletal-net.json';
        categoryName = 'Musculoskeletal Risk Network';
    } else if (pageName === 'cardiovascular') {
        dataFile = 'cardiovascular-net.json';
        categoryName = 'Cardiovascular Risk Network';
    } else if (pageName === 'immunology') {
        dataFile = 'immunology-net.json';
        categoryName = 'Immunology Risk Network';
    } else if (pageName === 'model-org') {
        dataFile = 'model-org-net.json';
        categoryName = 'Model Organism Biology Network';
    } else if (pageName === 'cross-cutting') {
        dataFile = 'cross-cutting-net.json';
        categoryName = 'CROSS-CUTTING INSIGHTS (Multi-Category Risks)';
    }

    // Update the main header to reflect the current category
    const categoryTitle = document.getElementById('category-title');
    if (categoryTitle) {
        categoryTitle.textContent = categoryName;
    }
    
    // 2. Fetch the determined JSON file
    fetch(dataFile)
        .then(response => {
            if (!response.ok) {
                throw new Error(`404: File not found at ${dataFile}. Check the filename and path.`);
            }
            return response.json();
        })
        .then(data => {
            // Check if resultsContainer exists before attempting to manipulate it
            const container = document.getElementById('text-results');

            // Display results in table format
            if (pageName === 'cross-cutting') {
                 displayCrossCuttingTextResults(data, container);
            } else {
                 displayStandardTextResults(data, container);
            }

            // Generate the graph
            const elements = buildCytoscapeElements(data, pageName);
            initializeCytoscape(elements);
        })
        .catch(error => {
            console.error('Error fetching or processing data:', error);
            const container = document.getElementById('text-results');
            if (container) {
                container.innerHTML = `<p class="error">Error loading data: ${error.message}</p>`;
            } else {
                console.error("Could not find text-results container.");
            }
        });

    // Initially hide the NLQ output section
    if (nlqOutput) {
        nlqOutput.style.display = 'none';
    }

    if (nlqButton) {
        nlqButton.addEventListener('click', () => {
            const userQuery = nlqInput.value.trim();
            if (!userQuery) {
                alert("Please enter a query.");
                return;
            }

            // 1. Hide the main page content, show NLQ output section
            if (mainContent) {
                mainContent.style.display = 'none';
            }
            if (nlqOutput) {
                nlqOutput.style.display = 'block';
            }

            // 2. Display the processing message
            nlqOutput.innerHTML = `
                <p style="color: #FF6C00; font-weight: bold;">Processing NLQ: "${userQuery}"...</p>
                <div style="height: 500px; display: flex; align-items: center; justify-content: center;">
                    <p>Translating query using AI and searching Knowledge Graph...</p>
                </div>
            `;

            // 3. Simulate the result after a brief delay
            setTimeout(() => {
                let simTitle = 'Simulated Results: Radiation Risks in Small Organisms';
                if (userQuery.toLowerCase().includes('cardio')) {
                     simTitle = 'Simulated Results: Cardiovascular Risks in Human Cells';
                }

                nlqOutput.innerHTML = `
                    <h2 style="color: #002D62; border-bottom: 3px solid #FF6C00;">${simTitle}</h2>
                    <div style="display: flex; gap: 30px; flex-wrap: wrap;">
                        <div style="flex: 1 1 40%; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.15); overflow-x: auto;">
                            <p style="font-weight: bold;">Simulated Table Data:</p>
                            <table>
                                <thead>
                                    <tr><th>Phenotype</th><th>Organisms</th><th>Source</th></tr>
                                </thead>
                                <tbody>
                                    <tr><td>DNA Damage & Repair Defect</td><td>C. elegans, Yeast, Human cell line</td><td>PMID:12345</td></tr>
                                    <tr><td>Metabolic Dysfunction</td><td>C. elegans, Yeast</td><td>PMID:67890</td></tr>
                                    <tr><td>Muscle Atrophy</td><td>Mus musculus</td><td>PMID:11223</td></tr>
                                </tbody>
                            </table>
                        </div>
                        <div id="simulated-cy" style="flex: 1 1 55%; min-height: 450px; background: #fdfdfd; border: 1px solid #ddd; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.15);">
                            </div>
                    </div>
                    <button onclick="document.getElementById('main-dashboard-content').style.display='flex'; document.getElementById('nlq-output').style.display='none';" 
                            style="margin-top: 20px; padding: 10px 20px; background-color: #002D62; color: white; border: none; border-radius: 4px; cursor: pointer;">
                        Back to Main Dashboard
                    </button>
                `;

                // ⭐ Initialize a small, static Cytoscape graph in the simulated div ⭐
                const simulatedElements = [
                    { data: { id: 'P_DNADamage', label: 'DNA Damage', type: 'phenotype', organismCount: 3 } },
                    { data: { id: 'P_MetabolicDysfunction', label: 'Metabolic Dysfunction', type: 'phenotype', organismCount: 2 } },
                    { data: { id: 'O_CElegans', label: 'C. elegans', type: 'organism' } },
                    { data: { id: 'O_Yeast', label: 'Yeast', type: 'organism' } },
                    { data: { id: 'O_HumanCellLine', label: 'Human Cell', type: 'organism' } },
                    { data: { id: 'E1', source: 'O_CElegans', target: 'P_DNADamage', type: 'exhibits' } },
                    { data: { id: 'E2', source: 'O_Yeast', target: 'P_DNADamage', type: 'exhibits' } },
                    { data: { id: 'E3', source: 'O_HumanCellLine', target: 'P_DNADamage', type: 'exhibits' } },
                    { data: { id: 'E4', source: 'O_CElegans', target: 'P_MetabolicDysfunction', type: 'exhibits' } },
                    { data: { id: 'E5', source: 'O_Yeast', target: 'P_MetabolicDysfunction', type: 'exhibits' } }
                ];
                
                // Call a modified Cytoscape initialization function for the simulated graph
                initializeSimulatedCytoscape(simulatedElements, 'simulated-cy');

            }, 2000); // 2-second simulation delay
        });
    }
});

// simulated NLQ graph 
function initializeSimulatedCytoscape(elements, containerId) {
    const cySim = cytoscape({
        container: document.getElementById(containerId),
        elements: elements,
        style: [
            {
                selector: 'node',
                style: {
                    'label': 'data(label)',
                    'text-valign': 'center',
                    'color': 'white',
                    'font-size': '12px',
                    'text-wrap': 'wrap',
                    'text-max-width': '80px',
                    'text-halign': 'center'
                }
            },
            {
                selector: 'node[type="phenotype"]',
                style: {
                    'background-color': '#FF6C00', 
                    'width': 'mapData(organismCount, 1, 3, 50, 80)', // Scale for small graph
                    'height': 'mapData(organismCount, 1, 3, 50, 80)',
                }
            },
            {
                selector: 'node[type="organism"]',
                style: {
                    'background-color': '#002D62', 
                    'shape': 'round-rectangle',
                    'padding': '10px'
                }
            },
            {
                selector: 'edge', // Generic edge style for simplicity in simulation
                style: {
                    'width': 2,
                    'line-color': '#a0a0a0',
                    'target-arrow-shape': 'triangle',
                    'target-arrow-color': '#a0a0a0',
                    'curve-style': 'bezier'
                }
            },
            {
                selector: 'node:selected',
                style: {
                    'border-width': 3,
                    'border-color': 'black',
                    'overlay-padding': '6px',
                    'overlay-color': '#000000',
                    'overlay-opacity': 0.25
                }
            }
        ],
        layout: {
            name: 'cose', // Use cose for a more organized small graph
            idealEdgeLength: 80,
            nodeOverlap: 15,
            padding: 20,
            gravity: 10,
            numIter: 500,
            initialTemp: 100,
            coolingFactor: 0.9,
            minTemp: 1.0
        }
    });

    // Fit graph to container
    cySim.ready(function(){
        cySim.fit(cySim.elements(), 30);
    });
}

/**
 * Handles the table structure for the Cross-Cutting page (3 columns).
 */
function displayCrossCuttingTextResults(data, container) {
    if (!data || data.length === 0) {
        container.innerHTML = '<p>No phenotypes found that link two or more categories.</p>';
        return;
    }
    let html = '<table><thead><tr><th>Phenotype (Risk)</th><th>Organisms Involved</th><th>Categories Linked</th></tr></thead><tbody>';
    data.forEach(item => {
        html += `<tr><td>${item.Phenotype}</td><td>${item.Organisms.join(', ')}</td><td>${item.Categories.join(', ')}</td></tr>`;
    });
    html += '</tbody></table>';
    container.innerHTML = html;
}

/**
 * Handles the table structure for standard category pages (2 columns).
 */
function displayStandardTextResults(data, container) {
    if (!data || data.length === 0) {
        container.innerHTML = '<p>No cross-organism findings for this category.</p>';
        return;
    }
    let html = '<table><thead><tr><th>Phenotype (Risk)</th><th>Organisms Involved</th></tr></thead><tbody>';
    data.forEach(item => {
        html += `<tr><td>${item.Phenotype}</td><td>${item.Organisms.join(', ')}</td></tr>`;
    });
    html += '</tbody></table>';
    container.innerHTML = html;
}

/**
 * Builds the Cytoscape elements array from the JSON data.
 */
/**
 * Builds the Cytoscape elements array from the JSON data.
 */
function buildCytoscapeElements(data, pageName) {
    const elements = [];
    const phenotypeIds = new Set();
    const organismIds = new Set();
    const categoryIds = new Set();

    data.forEach(item => {
        const phenotypeId = `P_${item.Phenotype.replace(/\s/g, '_')}`;
        const organismCount = item.OrganismCount || item.Organisms.length; // Use the count from Cypher or calculate it

        // 1. Phenotype Node (Always present)
        if (!phenotypeIds.has(phenotypeId)) {
            let label = item.Phenotype;
            if (label.length > 50) {
                label = label.substring(0, 50) + '...'; // Truncate long labels
            }
            elements.push({
                data: { 
                    id: phenotypeId, 
                    label: label, 
                    type: 'phenotype',
                    // ⭐ ADD ORGANISM COUNT FOR CENTRALITY ⭐
                    organismCount: organismCount 
                }
            });
            phenotypeIds.add(phenotypeId);
        }

        // 2. Organism Nodes and Edges
        item.Organisms.forEach(org => {
            const orgId = `O_${org.replace(/\s/g, '_')}`;
            if (!organismIds.has(orgId)) {
                elements.push({
                    data: { 
                        id: orgId, 
                        label: org, 
                        type: 'organism' 
                    }
                });
                organismIds.add(orgId);
            }
            // Edge from Organism to Phenotype
            elements.push({
                data: {
                    id: `E_${orgId}_${phenotypeId}`,
                    source: orgId,
                    target: phenotypeId,
                    type: 'exhibits'
                }
            });
        });

        // 3. Category Nodes and Edges (Only for cross-cutting view)
        if (pageName === 'cross-cutting' && item.Categories) {
            item.Categories.forEach(cat => {
                const catId = `C_${cat.replace(/\s/g, '_')}`;
                if (!categoryIds.has(catId)) {
                    elements.push({
                        data: { 
                            id: catId, 
                            label: cat, 
                            type: 'category' 
                        }
                    });
                    categoryIds.add(catId);
                }
                // Edge from Phenotype to Category
                elements.push({
                    data: {
                        id: `E_${phenotypeId}_${catId}`,
                        source: phenotypeId,
                        target: catId,
                        type: 'belongs_to'
                    }
                });
            });
        }
    });

    return elements;
}

/**
 * Initializes and styles the Cytoscape graph.
 */
/**
 * Initializes and styles the Cytoscape graph.
 */
function initializeCytoscape(elements) {
    const layout = elements.length > 50 ? 'cose' : 'circle'; // Dynamic layout choice

    const cy = cytoscape({
        container: document.getElementById('cy'),
        elements: elements,
        style: [
            // Node Styles
            {
                selector: 'node',
                style: {
                    'label': 'data(label)',
                    'text-valign': 'center',
                    'color': 'white',
                    'font-size': '12px', // Increased font size for better visibility
                    'text-wrap': 'wrap',
                    'text-max-width': '80px', // Prevents labels from getting too wide
                    'text-halign': 'center'
                }
            },
            {
                selector: 'node[type="phenotype"]',
                style: {
                    'background-color': '#FF6C00', 
                    // ⭐ DYNAMICALLY SCALE SIZE BASED ON ORGANISM COUNT ⭐
                    'width': 'mapData(organismCount, 1, 10, 50, 100)', 
                    'height': 'mapData(organismCount, 1, 10, 50, 100)',
                    // The above mapping means:
                    // If organismCount is 1, size is 50px.
                    // If organismCount is 10 or more, size is 100px.
                }
            },
            {
                selector: 'node[type="organism"]',
                style: {
                    'background-color': '#002D62', // NASA Blue for Primary Entity
                    'shape': 'round-rectangle',
                    'padding': '10px'
                }
            },
            {
                selector: 'node[type="category"]',
                style: {
                    'background-color': '#1CB76E', // Secondary accent color for Category
                    'shape': 'star',
                    'width': '80px',
                    'height': '80px'
                }
            },
            // Edge Styles
            {
                selector: 'edge[type="exhibits"]',
                style: {
                    'width': 2,
                    'line-color': '#a0a0a0',
                    'target-arrow-shape': 'triangle',
                    'target-arrow-color': '#a0a0a0',
                    'curve-style': 'bezier'
                }
            },
            {
                selector: 'edge[type="belongs_to"]',
                style: {
                    'width': 3,
                    'line-color': '#FF6C00',
                    'target-arrow-shape': 'vee',
                    'target-arrow-color': '#FF6C00',
                    'curve-style': 'bezier'
                }
            },
            // Hover/Selection Styles
            {
                selector: 'node:selected',
                style: {
                    'border-width': 3,
                    'border-color': 'black',
                    'overlay-padding': '6px',
                    'overlay-color': '#000000',
                    'overlay-opacity': 0.25
                }
            }
        ],
        layout: {
            name: layout,
            idealEdgeLength: 100,
            nodeOverlap: 20,
            randomize: true,
            componentSpacing: 40,
            nodeRepulsion: function( node ){ return 400000; },
            edgeElasticity: function( edge ){ return 100; },
            gravity: 80,
            numIter: 1000,
            coolingFactor: 0.95,
            minTemp: 1.0
        }
    });

    // --- ⭐ ADD HOVER (TOOLTIP) FUNCTIONALITY ⭐ ---
    
    // Create a temporary element for the tooltip display
    const tooltip = document.createElement('div');
    tooltip.style.position = 'absolute';
    tooltip.style.backgroundColor = 'rgba(0, 0, 0, 0.8)';
    tooltip.style.color = 'white';
    tooltip.style.padding = '5px 8px';
    tooltip.style.borderRadius = '3px';
    tooltip.style.zIndex = '1000';
    tooltip.style.pointerEvents = 'none'; // Essential: prevents interference with graph interaction
    tooltip.style.display = 'none';
    document.getElementById('cy').appendChild(tooltip);

    cy.on('mouseover', 'node', function(event) {
        const node = event.target;
        const labelText = node.data('label');
        
        // Use the original, untruncated name if possible (requires storing it in data)
        // For now, we use the visible label text
        tooltip.textContent = labelText; 
        tooltip.style.display = 'block';
        
        // Position the tooltip near the mouse/node
        const viewportPos = event.renderedPosition;
        tooltip.style.left = `${viewportPos.x + 15}px`;
        tooltip.style.top = `${viewportPos.y - 15}px`;
    });

    cy.on('mouseout', 'node', function() {
        tooltip.style.display = 'none';
    });
    
    // Fit graph to container
    cy.ready(function(){
        cy.fit(cy.elements(), 30); // zoom out by 30 pixels
    });
}