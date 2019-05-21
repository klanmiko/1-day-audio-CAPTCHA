function analyze(filename)
    [y, Fs] = audioread(filename);
    [len, ~] = size(y);
    windowsize = 50;
    w = hamming(windowsize);
    
    windows = len - windowsize;
    
    ste = zeros(1, windows);
    staa = ste;
    zcr = ste;
    
    for i = 1:windows
        Si = y(i:i+windowsize-1, 1) .* w;
        ste(i) = sum(Si.^2);
        staa(i) = mean(Si);        
        zcr(i) = mean(abs(diff(sign(Si))));      
    end
    
    plot(1:windows, ste);
    figure;
    plot(1:windows, staa);
    figure;
    plot(1:windows, zcr);
    figure;
    plot(1:len, y(:, 1));
    figure;

end

