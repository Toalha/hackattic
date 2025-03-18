#include <iostream>

std::string compress_string(const std::string input){
    std::string output{};
    int repeated{1};
    char lastchar;
    
    for(int it = 0; it < input.size(); it++){
        if(it == input.size() - 1){
            if(input[it] == lastchar){
                output.append(std::to_string(++repeated));
                output.push_back(lastchar);
            }
            else{
                output.append(std::to_string(repeated));
                output.push_back(lastchar);
                output.push_back(input[it]);
            }
        }
        else if(it == 0){
            lastchar = input[0];
            repeated = 1;
        }
        else{
            if(input[it] == lastchar){
                repeated++;
            }
            else{
                if(repeated > 1){
                    output.append(std::to_string(repeated));
                }
                output.push_back(lastchar);
                repeated = 1;
                lastchar = input[it];
            }
        }
    }
    return output;
}

int main() {
    std::string input{};
    while(true){
      std::cin >> input;
      
      input = compress_string(input);
      
      std::cout << input << std::endl;
      
      
    }
    return 0;
}
