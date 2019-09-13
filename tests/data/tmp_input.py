tmp_string = """
// Initial random seed:
1806669780843

// RunInitializeCallbacks():
initializeMutationRate(1e-05);
initializeMutationType(1, 0.5, "n", 0, 0.05);
initializeGenomicElementType(1, m1, 1);
initializeGenomicElement(g1, 20001, 20002);
initializeGenomicElement(g1, 27501, 27502);
initializeGenomicElement(g1, 132501, 132502);
initializeGenomicElement(g1, 140001, 140002);
(...initializeGenomicElement() calls omitted...)
initializeRecombinationRate(1e-05);

// Starting run at generation <start>:
1 

"position select_coef p1_freq p2_freq fixed_since migr_rate mut_rate recomb_rate fitness_width output_gen 
20001 -0.020159 0 283 370 1e-05 1e-05 1e-05 5 500
20001 0.0116518 20 0 468 1e-05 1e-05 1e-05 5 500
"
"position select_coef p1_freq p2_freq fixed_since migr_rate mut_rate recomb_rate fitness_width output_gen 
20001 -0.020159 0 23 370 1e-05 1e-05 1e-05 5 1000
20002 0.13452 18 0 964 1e-05 1e-05 1e-05 5 1000
27502 -0.00283611 0 61 477 1e-05 1e-05 1e-05 5 1000
140001 -0.0744118 2 0 994 1e-05 1e-05 1e-05 5 1000
"
"position select_coef p1_freq p2_freq fixed_since migr_rate mut_rate recomb_rate fitness_width output_gen 
20001 -0.0191989 1 0 1499 1e-05 1e-05 1e-05 5 1500
20002 0.0196835 1 0 1500 1e-05 1e-05 1e-05 5 1500
"
"""