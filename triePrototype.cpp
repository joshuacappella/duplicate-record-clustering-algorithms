#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <unordered_map>
#include <algorithm>

// Trie Node Structure
struct TrieNode {
    std::unordered_map<char, TrieNode*> children;
    int clusterId = -1; // -1 indicates no cluster
};

// Trie Class
class Trie {
public:
    TrieNode* root;

    Trie() : root(new TrieNode()) {}

    void insert(const std::string& word, int clusterId) {
        TrieNode* node = root;
        for (size_t i = 0; i < 3 && i < word.length(); ++i) {
            char c = word[i];
            if (node->children.find(c) == node->children.end()) {
                node->children[c] = new TrieNode();
            }
            node = node->children[c];
        }
        node->clusterId = clusterId;
    }

    int findCluster(const std::string& word) const {
        const TrieNode* node = root;
        for (size_t i = 0; i < 3 && i < word.length(); ++i) {
            char c = word[i];
            if (node->children.find(c) == node->children.end()) {
                return -1; // Not found
            }
            node = node->children.at(c);
        }
        return node->clusterId;
    }

    ~Trie() {
        // Simple recursive deletion (can be optimized for large tries)
        std::function<void(TrieNode*)> deleteTrie = [&](TrieNode* node) {
            if (node) {
                for (auto& pair : node->children) {
                    deleteTrie(pair.second);
                }
                delete node;
            }
        };
        deleteTrie(root);
    }
};

// Function to read data from CSV
/*std::vector<std::string> readFirstColumnFromCSV(const std::string& filename, int maxRows) {
    std::vector<std::string> columnData;
    std::ifstream file(filename);

    if (!file.is_open()) {
        std::cerr << "Error: Could not open file " << filename << std::endl;
        return columnData;
    }

    std::string line;
    int rowCount = 0;

    while (std::getline(file, line) && rowCount < maxRows) {
        std::stringstream ss(line);
        std::string cell;

        if (std::getline(ss, cell, ',')) {
            columnData.push_back(cell);
        } else {
            columnData.push_back("");
        }
        rowCount++;
    }

    file.close();
    return columnData;
}*/

std::vector<std::string> readColumnFromCSV(const std::string& filename, int columnIndex, int maxRows = -1) {
    std::vector<std::string> columnData;
    std::ifstream file(filename);

    if (!file.is_open()) {
        std::cerr << "Error: Could not open file " << filename << std::endl;
        return columnData;
    }

    std::string line;
    int rowCount = 0;

    while (std::getline(file, line) && (maxRows == -1 || rowCount < maxRows)) {
        std::stringstream ss(line);
        std::string cell;
        int currentColumn = 0;

        while (std::getline(ss, cell, ',')) {
            if (currentColumn == columnIndex) {
                columnData.push_back(cell);
                break;
            }
            currentColumn++;
        }
        if (currentColumn <= columnIndex){
            columnData.push_back("");
        }
        rowCount++;
    }

    file.close();
    return columnData;
}

// Function to cluster strings using Trie
std::unordered_map<std::string, int> clusterStrings(const std::vector<std::string>& data) {
    Trie trie;
    std::unordered_map<std::string, int> clusterAssignments;
    std::unordered_map<std::string, int> prefixClusters;
    int clusterId = 0;

    for (const std::string& word : data) {
        std::string prefix = word.substr(0, std::min(3UL, word.length())); // handles words shorter than 3 chars.
        if (prefixClusters.find(prefix) == prefixClusters.end()) {
            prefixClusters[prefix] = clusterId++;
        }
        trie.insert(word, prefixClusters[prefix]);
    }

    for (const std::string& word : data) {
        clusterAssignments[word] = trie.findCluster(word);
    }

    return clusterAssignments;
}

int main() {
    std::string filename = "";
    int columnIndex = -1;
    std::cout << "Type in name of file for analysis: " << std::endl;
    std::cin >> filename;
    std::cout << std::endl << "Type in the column number you would like to cluster: " << std::endl;
    std::cin >> columnIndex;
    std::cout << std::endl;
    //const std::string filename = "RandomNames.csv"; // Replace with your CSV file name
    const int maxRows = 42;

    //std::vector<std::string> data = readFirstColumnFromCSV(filename, maxRows);
    std::vector<std::string> data = readColumnFromCSV(filename, columnIndex, maxRows);
    std::unordered_map<std::string, int> clusters = clusterStrings(data);

    int clusterQuantity = 1;
    int totalClusters = 0;
    int oldClusterNum = 0;
    std::string oldClusterName = "";
    std::vector<int> clusterCounts(maxRows, 0);

    std::cout << std::endl;

    for (const auto& pair : clusters) {
        if (pair.second != oldClusterNum && clusterCounts.at(oldClusterNum) > 1){
            std::cout << "First 3 letters in name: " << oldClusterName.substr(0, 3) << std::endl;
            std::cout << clusterCounts.at(oldClusterNum) << " in Cluster " << oldClusterNum << std::endl << std:: endl;
        }
        clusterCounts.at(pair.second)++;
        oldClusterName = pair.first;
        oldClusterNum = pair.second;
    }

    for(int i = 0; i < maxRows; i++){
        if(clusterCounts.at(i) > 1){
            totalClusters++;
        }
    }

    std::cout << "Number of clusters: " << totalClusters << std::endl << std::endl;

    return 0;
}