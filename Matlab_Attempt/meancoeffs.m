function meanified = meancoeffs(str)
    [y, Fs] = audioread(str);
    coeffs = mfcc(y, Fs);
    coeffs = coeffs(:, :, 1);
    meanified = mean(coeffs);
end

