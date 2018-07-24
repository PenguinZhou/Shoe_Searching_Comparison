file_txt = fopen('ration.txt','a')
file_mat = load('zappos-fg-rationale.mat')

for i = 1:4
    for j = 1:(length(file_mat.mturkHardRation{1, i}))
        ration_array = {}
        for k = 1:(length(file_mat.mturkHardRation{1, i}{j,1}))
            
            %ration_array = [ration_array, file_mat.mturkHardRation{1, i}{j,1}{1, k}]
        %ration_array = file_mat.mturkHardRation{1, i}{j, 1}
            if k < 6
                
                fprintf(file_txt, '%d ', file_mat.mturkHardRation{1, i}{j,1}{1, k})
            else
                fprintf(file_txt, '%s\r\n', file_mat.mturkHardRation{1, i}{j,1}{1, k})
            end
        %dlmwrite('ration.csv', ration_array, '-append')
        end
        
    end
end

fclose(file_txt)
