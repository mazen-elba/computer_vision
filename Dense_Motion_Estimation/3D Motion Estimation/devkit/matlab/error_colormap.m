function cols = error_colormap ()
    % color changes at 1
    
    cols = [ 0/3.0,       0.1875/3.0,  49,  54, 149;
             0.1875/3.0,  0.375/3.0,   69, 117, 180;
             0.375/3.0,   0.75/3.0,   116, 173, 209;
             0.75/3.0,    1.5/3.0,    171, 217, 233;
             1.5/3.0,     3/3.0,      224, 243, 248;
             3/3.0,       6/3.0,      254, 224, 144;
             6/3.0,      12/3.0,      253, 174,  97;
            12/3.0,      24/3.0,      244, 109,  67;
            24/3.0,      48/3.0,      215,  48,  39;
            48/3.0,     inf,      165,   0,  38 ];
          
    cols(:,3:5) = cols(:,3:5)/255;