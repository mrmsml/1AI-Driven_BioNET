import pandas as pd
from neo4j import GraphDatabase

# =========================================================================
# 1. NEO4J CONNECTION DETAILS
# =========================================================================
# IMPORTANT: Update the password below with your actual Neo4j password
URI = "bolt://localhost:7687"
AUTH = ("neo4j", "v8XCgsNiRuWDAPD") 

# =========================================================================
# 2. SIMULATED DATA (Based on Step 1)
# =========================================================================
# This list simulates the structured output of the NLP/extraction pipeline
TRIPLETS_DATA = [
    # -----------------------------------------------------------
    # CATEGORY 1: MUSCULOSKELETAL RISKS (Bone & Muscle Loss)
    # -----------------------------------------------------------
    {'source_id': 'P001', 'title': 'Mice in Bion-M 1 space mission: training and selection', 'organism': 'Mus musculus', 'phenotype': 'Physiological Deconditioning', 'category': 'Musculoskeletal'},
    {'source_id': 'P002', 'title': 'Microgravity induces pelvic bone loss through osteoclastic activity', 'organism': 'Mus musculus', 'phenotype': 'Pelvic Bone Loss', 'category': 'Musculoskeletal'},
    {'source_id': 'P002', 'title': 'Microgravity induces pelvic bone loss...', 'organism': 'Osteoblasts/Osteoclasts', 'phenotype': 'Inhibited Cell Cycle (CDKN1a)', 'category': 'Musculoskeletal'},
    {'source_id': 'P007', 'title': 'Dose- and Ion-Dependent Effects in the Oxidative Stress Response...', 'organism': 'Skeletal System', 'phenotype': 'Oxidative Stress Response', 'category': 'Musculoskeletal'},
    {'source_id': 'P010', 'title': 'Effects of ex vivo ionizing radiation on collagen structure...', 'organism': 'Mouse Vertebrae', 'phenotype': 'Collagen Structure Alteration', 'category': 'Musculoskeletal'},
    {'source_id': 'P011', 'title': 'Absence of gamma-sarcoglycan alters the response of p70S6 kinase...', 'organism': 'Murine Skeletal Muscle', 'phenotype': 'Altered Muscle Response to Load', 'category': 'Musculoskeletal'},
    {'source_id': 'P027', 'title': 'Muscle atrophy phenotype gene expression during spaceflight...', 'organism': 'Mus musculus', 'phenotype': 'Muscle Atrophy', 'category': 'Musculoskeletal'},
    {'source_id': 'P041', 'title': 'Microgravity Stress: Bone and Connective Tissue', 'organism': 'Connective Tissue', 'phenotype': 'Tissue Degradation', 'category': 'Musculoskeletal'},
    {'source_id': 'P054', 'title': 'Partial weight suspension: A novel murine model...', 'organism': 'Mus musculus', 'phenotype': 'Reduced Musculoskeletal Loading', 'category': 'Musculoskeletal'},
    {'source_id': 'P055', 'title': 'Partial reductions in mechanical loading yield proportional changes...', 'organism': 'Mus musculus', 'phenotype': 'Proportional Bone Density Loss', 'category': 'Musculoskeletal'},
    {'source_id': 'P056', 'title': 'Spaceflight and hind limb unloading induce similar changes...', 'organism': 'Mouse Gastrocnemius Muscle', 'phenotype': 'Altered Electrical Impedance', 'category': 'Musculoskeletal'},
    {'source_id': 'P058', 'title': 'Treatment with a soluble bone morphogenetic protein type 1A...', 'organism': 'Mus musculus', 'phenotype': 'Increased Bone Mass', 'category': 'Musculoskeletal'},
    {'source_id': 'P059', 'title': 'RNAseq and RNA molecular barcoding reveal differential gene expression...', 'organism': 'Female Mice (Cortical Bone)', 'phenotype': 'Altered Gene Expression (Bone)', 'category': 'Musculoskeletal'},
    {'source_id': 'P077', 'title': 'Toward countering muscle and bone loss with spaceflight...', 'organism': 'Musculoskeletal System', 'phenotype': 'Muscle/Bone Loss', 'category': 'Musculoskeletal'},
    {'source_id': 'P078', 'title': 'Spaceflight increases sarcoplasmic reticulum Ca2+ leak...', 'organism': 'Skeletal Muscle', 'phenotype': 'Increased Ca2+ Leak (Muscle)', 'category': 'Musculoskeletal'},
    {'source_id': 'P094', 'title': 'Articular cartilage and sternal fibrocartilage respond differently...', 'organism': 'Cartilage', 'phenotype': 'Microgravity-Specific Tissue Response', 'category': 'Musculoskeletal'},
    {'source_id': 'P100', 'title': 'Low-dose, ionizing radiation and age-related changes...', 'organism': 'Skeletal Microarchitecture', 'phenotype': 'Age-Related Bone Changes', 'category': 'Musculoskeletal'},
    {'source_id': 'P101', 'title': 'Ionizing Radiation Stimulates Expression of Pro-Osteoclastogenic Genes...', 'organism': 'Skeletal Tissue/Marrow', 'phenotype': 'Pro-Osteoclastogenic Gene Expression', 'category': 'Musculoskeletal'},
    
    # -----------------------------------------------------------
    # CATEGORY 2: CARDIOVASCULAR RISKS (Heart, Vessels, Circulation)
    # -----------------------------------------------------------
    {'source_id': 'P006', 'title': 'Spaceflight Modulates the Expression of Key Oxidative Stress...', 'organism': 'Heart Tissue', 'phenotype': 'Oxidative Stress Response', 'category': 'Cardiovascular'},
    {'source_id': 'P021', 'title': 'GeneLab database analyses suggest long-term impact of space radiation...', 'organism': 'Cardiovascular System', 'phenotype': 'Radiation-Induced FYN Activation', 'category': 'Cardiovascular'},
    {'source_id': 'P060', 'title': 'Proteomic and phosphoproteomic characterization of cardiovascular tissues...', 'organism': 'Cardiovascular Tissues', 'phenotype': 'Radiation-Induced Proteomic Changes', 'category': 'Cardiovascular'},
    {'source_id': 'P079', 'title': 'Cardiovascular progenitor cells cultured aboard the ISS...', 'organism': 'Cardiovascular Progenitor Cells', 'phenotype': 'Altered Developmental Properties', 'category': 'Cardiovascular'},
    {'source_id': 'P086', 'title': 'Chronic skeletal unloading of the rat femur: vascular remodeling...', 'organism': 'Rat Femur', 'phenotype': 'Vascular Remodeling', 'category': 'Cardiovascular'},
    {'source_id': 'P088', 'title': 'Effects of spaceflight and ground recovery on mesenteric artery...', 'organism': 'Mouse Arteries/Veins', 'phenotype': 'Altered Vasoconstrictor Properties', 'category': 'Cardiovascular'},
    {'source_id': 'P089', 'title': 'Spaceflight-induced alterations in cerebral artery...', 'organism': 'Cerebral Artery', 'phenotype': 'Elevated Intracranial Pressure Risk', 'category': 'Cardiovascular'},
    {'source_id': 'P091', 'title': 'Effects of Skeletal Unloading on the Vasomotor Properties...', 'organism': 'Rat Femur (Artery)', 'phenotype': 'Altered Vasomotor Properties', 'category': 'Cardiovascular'},
    {'source_id': 'P093', 'title': 'Spaceflight on the Bion-M1 biosatellite alters cerebral artery...', 'organism': 'Mus musculus', 'phenotype': 'Altered Cerebral Artery Properties', 'category': 'Cardiovascular'},
    {'source_id': 'P094', 'title': 'Apollo Lunar Astronauts Show Higher Cardiovascular Disease Mortality...', 'organism': 'Homo sapiens (Astronauts)', 'phenotype': 'Increased CVD Mortality Risk', 'category': 'Cardiovascular'},
    {'source_id': 'P096', 'title': 'Simulated microgravity induces regionally distinct neurovascular...', 'organism': 'Rat Skeletal Muscle Artery', 'phenotype': 'Neurovascular Remodeling', 'category': 'Cardiovascular'},
    {'source_id': 'P103', 'title': 'Redox Signaling and Its Impact on Skeletal and Vascular Responses...', 'organism': 'Skeletal and Vascular Systems', 'phenotype': 'Altered Redox Signaling', 'category': 'Cardiovascular'},
    
    # -----------------------------------------------------------
    # CATEGORY 3: IMMUNOLOGY RISKS (Infection, Inflammation, Immunity)
    # -----------------------------------------------------------
    {'source_id': 'P019', 'title': 'Toll mediated infection response is altered by gravity...', 'organism': 'Drosophila', 'phenotype': 'Altered Toll Infection Response', 'category': 'Immunology'},
    {'source_id': 'P033', 'title': 'Innate immune responses of Drosophila melanogaster are altered...', 'organism': 'Drosophila', 'phenotype': 'Altered Innate Immune Response', 'category': 'Immunology'},
    {'source_id': 'P042', 'title': 'S. aureus MscL is a pentamer in vivo...', 'organism': 'Staphylococcus aureus', 'phenotype': 'Altered Protein Stoichiometry (MscL)', 'category': 'Immunology'},
    {'source_id': 'P047', 'title': 'The MscS and MscL families of mechanosensitive channels...', 'organism': 'Microbial (General)', 'phenotype': 'Osmotic Stress Response', 'category': 'Immunology'},
    {'source_id': 'P081', 'title': 'Genomic and functional characterization of Enterococcus faecalis...', 'organism': 'Enterococcus faecalis', 'phenotype': 'Potential for Pathogenicity', 'category': 'Immunology'},
    {'source_id': 'P082', 'title': 'Evaluation of in vitro macrophage differentiation during space flight.', 'organism': 'Macrophages', 'phenotype': 'Impaired Differentiation', 'category': 'Immunology'},
    {'source_id': 'P084', 'title': 'Understanding macrophage differentiation during space flight...', 'organism': 'Macrophages', 'phenotype': 'Altered Differentiation', 'category': 'Immunology'},
    {'source_id': 'P085', 'title': 'Bone marrow leptin signaling mediates obesity-associated...', 'organism': 'Murine Macrophages', 'phenotype': 'Adipose Tissue Inflammation', 'category': 'Immunology'},
    {'source_id': 'P087', 'title': 'Validation of methods to assess the immunoglobulin gene repertoire...', 'organism': 'Mus musculus', 'phenotype': 'Altered Immunoglobulin Repertoire', 'category': 'Immunology'},
    {'source_id': 'P090', 'title': 'Effects of spaceflight on the immunoglobulin repertoire...', 'organism': 'Mus musculus', 'phenotype': 'Altered Antibody Repertoire', 'category': 'Immunology'},
    {'source_id': 'P099', 'title': 'Spaceflight promotes biofilm formation by Pseudomonas aeruginosa.', 'organism': 'Pseudomonas aeruginosa', 'phenotype': 'Enhanced Biofilm Formation', 'category': 'Immunology'},
    {'source_id': 'P105', 'title': 'Overexpression of catalase in mitochondria mitigates changes...', 'organism': 'Hippocampal Tissue', 'phenotype': 'Altered Cytokine Expression', 'category': 'Immunology'},
    {'source_id': 'P109', 'title': 'Spaceflight and simulated microgravity conditions increase virulence...', 'organism': 'Serratia marcescens', 'phenotype': 'Increased Virulence', 'category': 'Immunology'},
    {'source_id': 'P112', 'title': 'Simultaneous exposure of cultured human lymphoblastic cells...', 'organism': 'Human Lymphoblastic Cells', 'phenotype': 'Increased Chromosome Aberrations', 'category': 'Immunology'},
    
    # -----------------------------------------------------------
    # CATEGORY 4: MODEL ORGANISM BIOLOGY (Plants, Invertebrates, Microbes, etc.)
    # -----------------------------------------------------------
    {'source_id': 'P003', 'title': 'Stem Cell Health and Tissue Regeneration in Microgravity', 'organism': 'Embryonic Stem Cells', 'phenotype': 'Altered Regeneration Potential', 'category': 'Model Organism Biology'},
    {'source_id': 'P004', 'title': 'Microgravity Reduces the Differentiation and Regenerative Potential...', 'organism': 'Embryonic Stem Cells', 'phenotype': 'Reduced Differentiation', 'category': 'Model Organism Biology'},
    {'source_id': 'P005', 'title': 'Microgravity validation of a novel system for RNA isolation...', 'organism': 'Cell Culture (General)', 'phenotype': 'Gene Expression Analysis (Method)', 'category': 'Model Organism Biology'},
    {'source_id': 'P012', 'title': 'AtRabD2b and AtRabD2c have overlapping functions in pollen development...', 'organism': 'Arabidopsis thaliana (Pollen)', 'phenotype': 'Pollen Tube Growth', 'category': 'Model Organism Biology'},
    {'source_id': 'P013', 'title': 'TNO1 is involved in salt tolerance and vacuolar trafficking...', 'organism': 'Arabidopsis thaliana', 'phenotype': 'Salt Tolerance Modulation', 'category': 'Model Organism Biology'},
    {'source_id': 'P015', 'title': 'Root growth movements: Waving and skewing.', 'organism': 'Arabidopsis thaliana (Roots)', 'phenotype': 'Waving and Skewing Movement', 'category': 'Model Organism Biology'},
    {'source_id': 'P016', 'title': 'Gravitropism and lateral root emergence are dependent on the TNO1', 'organism': 'Arabidopsis thaliana', 'phenotype': 'Altered Gravitropism', 'category': 'Model Organism Biology'},
    {'source_id': 'P017', 'title': 'TNO1, a TGN-localized SNARE-interacting protein, modulates root skewing...', 'organism': 'Arabidopsis thaliana', 'phenotype': 'Modulated Root Skewing', 'category': 'Model Organism Biology'},
    {'source_id': 'P018', 'title': 'The Drosophila SUN protein Spag4 cooperates with the coiled-coil...', 'organism': 'Drosophila', 'phenotype': 'Spermatid Nucleus Association', 'category': 'Model Organism Biology'},
    {'source_id': 'P020', 'title': 'Multi-omics analysis of multiple missions to space reveal a theme...', 'organism': 'Mouse Liver', 'phenotype': 'Lipid Dysregulation', 'category': 'Model Organism Biology'},
    {'source_id': 'P034', 'title': 'Prolonged Exposure to Microgravity Reduces Cardiac Contractility...', 'organism': 'Drosophila', 'phenotype': 'Reduced Cardiac Contractility', 'category': 'Model Organism Biology'},
    {'source_id': 'P049', 'title': 'Evidence for extensive horizontal gene transfer from the draft genome...', 'organism': 'Tardigrade (H. dujardini)', 'phenotype': 'Horizontal Gene Transfer', 'category': 'Model Organism Biology'},
    {'source_id': 'P051', 'title': 'Tardigrades Use Intrinsically Disordered Proteins to Survive Desiccation.', 'organism': 'Tardigrade', 'phenotype': 'Extreme Stress Tolerance', 'category': 'Model Organism Biology'},
    {'source_id': 'P061', 'title': 'Adaptive Changes in the Vestibular System of Land Snail...', 'organism': 'Land Snail', 'phenotype': 'Vestibular System Readaptation', 'category': 'Model Organism Biology'},
    {'source_id': 'P062', 'title': 'Morphology of the Utricular Otolith Organ in the Toadfish...', 'organism': 'Toadfish (Opsanus tau)', 'phenotype': 'Otolith Organ Morphology', 'category': 'Model Organism Biology'},
    {'source_id': 'P072', 'title': 'Relevance of the Unfolded Protein Response to Spaceflight-Induced...', 'organism': 'Arabidopsis thaliana', 'phenotype': 'Altered Transcriptional Reprogramming', 'category': 'Model Organism Biology'},
    {'source_id': 'P097', 'title': 'Impact of Spaceflight and Artificial Gravity on the Mouse Retina...', 'organism': 'Mus musculus (Retina)', 'phenotype': 'Biochemical/Proteomic Alterations', 'category': 'Model Organism Biology'},
    {'source_id': 'P106', 'title': 'An extensive allelic series of Drosophila kae1 mutants reveals...', 'organism': 'Drosophila', 'phenotype': 'Tissue-Specific Requirements (Gene)', 'category': 'Model Organism Biology'},
    {'source_id': 'P108', 'title': 'A combined computational strategy of sequence and structural analysis...', 'organism': 'Drosophila', 'phenotype': 'Functional Eicosanoid Pathway', 'category': 'Model Organism Biology'},
    {'source_id': 'P111', 'title': 'Drosophila parasitoids go to space: Unexpected effects...', 'organism': 'Drosophila / Parasitoid Wasp', 'phenotype': 'Unexpected Host/Parasitoid Effects', 'category': 'Model Organism Biology'},
    
    # -----------------------------------------------------------
    # CROSS-CUTTING (Radiation, CNS/SANS, Omics/Platform)
    # -----------------------------------------------------------
    {'source_id': 'P024', 'title': 'Circulating miRNA spaceflight signature reveals targets...', 'organism': 'Human/Mouse (General)', 'phenotype': 'Altered miRNA Signature', 'category': 'Cardiovascular'}, # Cross-Cut
    {'source_id': 'P026', 'title': 'Extraterrestrial Gynecology: Could Spaceflight Increase the Risk...', 'organism': 'Female Astronauts', 'phenotype': 'Increased Cancer Risk', 'category': 'Immunology'}, # Cross-Cut
    {'source_id': 'P028', 'title': 'Chromosomal positioning and epigenetic architecture...', 'organism': 'General', 'phenotype': 'Altered DNA Methylation (Radiation)', 'category': 'Immunology'}, # Cross-Cut
    {'source_id': 'P030', 'title': 'Aging and putative frailty biomarkers are altered by spaceflight', 'organism': 'Human/Mouse (General)', 'phenotype': 'Altered Aging/Frailty Biomarkers', 'category': 'Musculoskeletal'}, # Cross-Cut
    {'source_id': 'P031', 'title': 'Space radiation damage rescued by inhibition of key spaceflight...', 'organism': 'General', 'phenotype': 'Radiation Damage Rescue', 'category': 'Immunology'}, # Cross-Cut
    {'source_id': 'P074', 'title': 'Reanalysis of the Mars500 experiment reveals common gut microbiome...', 'organism': 'Homo sapiens (Crew)', 'phenotype': 'Gut Microbiome Alterations (Confinement)', 'category': 'Immunology'}, # Cross-Cut
    {'source_id': 'P075', 'title': 'High atomic weight, high-energy radiation (HZE) induces...', 'organism': 'Arabidopsis thaliana', 'phenotype': 'HZE-Specific Transcriptional Response', 'category': 'Model Organism Biology'}, # Cross-Cut
    {'source_id': 'P083', 'title': 'Identification of critical host mitochondrion-associated genes...', 'organism': 'Drosophila', 'phenotype': 'Host-Mitochondrion Genes (Infection)', 'category': 'Immunology'}, # Cross-Cut
    {'source_id': 'P095', 'title': 'Impact of Spaceflight and Artificial Gravity on the Mouse Retina...', 'organism': 'Mouse Retina', 'phenotype': 'Retinal Structural Alteration', 'category': 'Model Organism Biology'}, # Cross-Cut
    {'source_id': 'P104', 'title': 'Influence of social isolation during prolonged simulated weightlessness...', 'organism': 'Mus musculus', 'phenotype': 'Social Isolation Effects', 'category': 'Immunology'}, # Cross-Cut

    # -----------------------------------------------------------
    # CNS / VESTIBULAR / NEURO-OCULAR (SANS)
    # -----------------------------------------------------------
    {'source_id': 'P063', 'title': 'Influence of Magnitude and Duration of Altered Gravity...', 'organism': 'Toadfish (Opsanus tau)', 'phenotype': 'Altered Utricle Structure/Function', 'category': 'Model Organism Biology'},
    {'source_id': 'P097', 'title': 'Spaceflight decelerates the epigenetic clock orchestrated...', 'organism': 'Mus musculus (Retina)', 'phenotype': 'Epigenetic Clock Deceleration', 'category': 'Model Organism Biology'},
    {'source_id': 'P099', 'title': 'Development of otolith receptors in Japanese quail.', 'organism': 'Japanese Quail', 'phenotype': 'Otolith Receptor Development', 'category': 'Model Organism Biology'},
    {'source_id': 'P100', 'title': 'Spatial and temporal characteristics of vestibular convergence', 'organism': 'General', 'phenotype': 'Vestibular Convergence', 'category': 'Model Organism Biology'},
    {'source_id': 'P101', 'title': 'Bone remodeling is regulated by inner ear vestibular signals', 'organism': 'Vestibular System / Bone', 'phenotype': 'Vestibular Regulation of Bone', 'category': 'Musculoskeletal'}, # Cross-Cut
    {'source_id': 'P102', 'title': 'Simulated Microgravity Enhances Oligodendrocyte Mitochondrial Function...', 'organism': 'Oligodendrocytes', 'phenotype': 'Enhanced Mitochondrial Function', 'category': 'Model Organism Biology'},
    {'source_id': 'P103', 'title': 'Human Neural Stem Cells Flown into Space Proliferate...', 'organism': 'Human Neural Stem Cells', 'phenotype': 'Neurogenesis', 'category': 'Model Organism Biology'},
    {'source_id': 'P104', 'title': 'Delayed Maturation of Oligodendrocyte Progenitors by Microgravity...', 'organism': 'Oligodendrocyte Progenitors', 'phenotype': 'Delayed Maturation', 'category': 'Model Organism Biology'},
    {'source_id': 'P105', 'title': 'Space Microgravity Alters Neural Stem Cell Division...', 'organism': 'Neural Stem Cells', 'phenotype': 'Altered Cell Division', 'category': 'Model Organism Biology'},
    
    # -----------------------------------------------------------
    # PLANT & CELL BIOLOGY (Non-Human/Non-Invertebrate)
    # -----------------------------------------------------------
    {'source_id': 'P114', 'title': 'ERULUS is a plasma membrane-localized receptor-like kinase...', 'organism': 'Arabidopsis thaliana', 'phenotype': 'Root Hair Growth', 'category': 'Model Organism Biology'},
    {'source_id': 'P116', 'title': 'Cell type-specific imaging of calcium signaling in Arabidopsis...', 'organism': 'Arabidopsis thaliana (Roots)', 'phenotype': 'Calcium Signaling', 'category': 'Model Organism Biology'},
    {'source_id': 'P117', 'title': 'Spatial and temporal localization of SPIRRIG and WAVE/SCAR...', 'organism': 'Arabidopsis thaliana', 'phenotype': 'Actin-Mediated Root Development', 'category': 'Model Organism Biology'},
    {'source_id': 'P120', 'title': 'Host-microbe interactions in microgravity: assessment and implications.', 'organism': 'Host-Microbe Systems', 'phenotype': 'Altered Host-Microbe Interactions', 'category': 'Immunology'}, # Cross-Cut
    {'source_id': 'P125', 'title': 'Spaceflight alters host-gut microbiota interactions', 'organism': 'Human/Mouse (Gut)', 'phenotype': 'Altered Gut Microbiota Interactions', 'category': 'Immunology'}, # Cross-Cut
    {'source_id': 'P127', 'title': 'Comparative genomic analysis of Cohnella hashimotonis sp. nov....', 'organism': 'Cohnella hashimotonis (ISS)', 'phenotype': 'Genomic Characterization', 'category': 'Immunology'},
    {'source_id': 'P128', 'title': 'Characterization of metagenome-assembled genomes from the ISS', 'organism': 'ISS Metagenome', 'phenotype': 'Microbiome Characterization', 'category': 'Immunology'},
    {'source_id': 'P130', 'title': 'Extracellular nucleotides elicit cytosolic free calcium oscillations...', 'organism': 'Arabidopsis thaliana', 'phenotype': 'Cytosolic Calcium Oscillations', 'category': 'Model Organism Biology'},
    {'source_id': 'P133', 'title': 'Salt stress-induced Ca2+ waves are associated with rapid, long-distance...', 'organism': 'Arabidopsis thaliana', 'phenotype': 'Salt Stress Signaling (Ca2+)', 'category': 'Model Organism Biology'},
    {'source_id': 'P135', 'title': 'A ROS-assisted calcium wave dependent on AtRBOHD and TPC1...', 'organism': 'Arabidopsis thaliana (Roots)', 'phenotype': 'Systemic Salt Stress Response', 'category': 'Model Organism Biology'},
    {'source_id': 'P139', 'title': 'Tonoplast-localized Ca2+ pumps regulate Ca2+ signals during...', 'organism': 'Arabidopsis thaliana', 'phenotype': 'Regulated Immunity Signaling (Ca2+)', 'category': 'Immunology'},
    {'source_id': 'P140', 'title': 'The fast and the furious: Rapid long-range signaling in plants.', 'organism': 'Plants (General)', 'phenotype': 'Rapid Long-Range Signaling', 'category': 'Model Organism Biology'},
    {'source_id': 'P142', 'title': 'The vacuolar H+/Ca transporter CAX1 participates in submergence...', 'organism': 'Arabidopsis thaliana', 'phenotype': 'Submergence Stress Response', 'category': 'Model Organism Biology'},
    {'source_id': 'P143', 'title': 'Meta-analysis of the space flight and microgravity response...', 'organism': 'Arabidopsis thaliana', 'phenotype': 'Transcriptome Alterations', 'category': 'Model Organism Biology'},
    
    # -----------------------------------------------------------
    # OMICS PLATFORM / GENERAL METHODOLOGY
    # -----------------------------------------------------------
    {'source_id': 'P022', 'title': 'FAIRness and usability for open-access omics data systems.', 'organism': 'Data Systems', 'phenotype': 'FAIR Data Standards', 'category': 'Methodology'},
    {'source_id': 'P023', 'title': 'NASA GeneLab platform utilized for biological response...', 'organism': 'Data Systems', 'phenotype': 'Omics Data Utilization', 'category': 'Methodology'},
    {'source_id': 'P073', 'title': 'Genomic stability in response to high versus low linear energy...', 'organism': 'Arabidopsis thaliana', 'phenotype': 'Radiation Response (Genomic)', 'category': 'Model Organism Biology'},
    {'source_id': 'P098', 'title': 'Effect of spaceflight on Pseudomonas aeruginosa final cell density...', 'organism': 'Pseudomonas aeruginosa', 'phenotype': 'Density Modulated by Nutrients', 'category': 'Immunology'},
    {'source_id': 'P040', 'title': 'The biology of tardigrade disordered proteins in extreme stress...', 'organism': 'Tardigrade', 'phenotype': 'Intrinsically Disordered Proteins', 'category': 'Model Organism Biology'},
    
    # Additional Omics/CNS to reach ~100
    {'source_id': 'P144', 'title': 'Metabolomic profiling of the secretome from human neural stem cells...', 'organism': 'Human Neural Stem Cells', 'phenotype': 'Altered Metabolomic Profile', 'category': 'Model Organism Biology'},
    {'source_id': 'P145', 'title': 'Spatially resolved multiomics on the neuronal effects induced by spaceflight...', 'organism': 'Mus musculus (Brain)', 'phenotype': 'Neuronal Multiomics', 'category': 'Model Organism Biology'},
    {'source_id': 'P146', 'title': 'Comprehensive multi-omics analysis reveals mitochondrial stress...', 'organism': 'Multi-Species (Omics)', 'phenotype': 'Mitochondrial Stress (Central Hub)', 'category': 'Cardiovascular'},
    {'source_id': 'P147', 'title': 'Knowledge Network Embedding of Transcriptomic Data from Spaceflown Mice...', 'organism': 'Mus musculus', 'phenotype': 'Terrestrial Disease Association', 'category': 'Musculoskeletal'},
]


# =========================================================================
# 3. GRAPH INGESTION FUNCTIONS
# =========================================================================

# Initialize the Neo4j driver
try:
    driver = GraphDatabase.driver(URI, auth=AUTH)
    driver.verify_connectivity()
    print("✅ Neo4j connection successful.")
except Exception as e:
    print(f"❌ Failed to connect to Neo4j. Check credentials/URI. Error: {e}")
    exit()

# Define the Cypher query once
# Ingest_data.py

# Define the Cypher query with the new Category node
CREATE_TRIPLET_QUERY = """
    MERGE (p:Publication {id: $source_id})
    ON CREATE SET p.title = $title
    
    MERGE (o:Organism {name: $organism})
    MERGE (h:Phenotype {name: $phenotype})
    MERGE (c:Category {name: $category}) 
    
    // Connect the Phenotype to its Category
    CREATE (h)-[:BELONGS_TO]->(c) 
    // Existing connections
    CREATE (p)-[:REPORTS_FINDING_ON]->(o)
    CREATE (o)-[:EXHIBITS]->(h)
"""


def ingest_data(data):
    """Main function to iterate over data and run transactions using session.run()."""
    total_triplets = len(data)
    print(f"Starting ingestion of {total_triplets} triplets...")
    
    with driver.session() as session:
        # Clear the database before starting, just for PoC testing safety!
        session.run("MATCH (n) DETACH DELETE n")
        print("Database cleared for fresh ingestion.")

        # Execute the ingestion for each triplet using the corrected method
        for i, triplet in enumerate(data):
            session.run(CREATE_TRIPLET_QUERY, **triplet) # <-- FIX: Using session.run() directly
            if (i + 1) % 5 == 0:
                print(f"   Processed {i + 1}/{total_triplets} triplets...")
        
    print("=======================================================")
    print(f"🎉 INGESTION COMPLETE! {total_triplets} graph patterns loaded.")
    print("=======================================================")

# =========================================================================
# 4. EXECUTION
# =========================================================================
if __name__ == "__main__":
    ingest_data(TRIPLETS_DATA)
    driver.close()