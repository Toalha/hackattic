#include <stdio.h>
#include <string.h>
#include <openssl/evp.h>  // For Base64 decoding

// Function to swap bytes for endianness conversion
void swap_bytes(void* value, size_t size) {
    uint8_t* bytes = (uint8_t*)value;
    for (size_t i = 0; i < size / 2; i++) {
        uint8_t temp = bytes[i];
        bytes[i] = bytes[size - 1 - i];
        bytes[size - 1 - i] = temp;
    }
}

int main() {
    // Base64-encoded string
    char* b64encodedbytes = "vclfjAm4c/IjPgAAwy9PQy+oy89FDVtAQFsNRc/LqC8=";

    // Variables to store the unpacked values
    int int_ = 0; 
    unsigned int uint_ = 0;
    short int sint_ = 0;
    float float_ = 0.0;
    double double_ = 0.0; 
    double bigenddouble_ = 0.0;

    // Decode the Base64 string into binary data
    unsigned char decoded[128]; // Buffer bigger than necessary just in case
    int decoded_len = EVP_DecodeBlock(decoded, (unsigned char*)b64encodedbytes, strlen(b64encodedbytes));
    if (decoded_len < 0) {
        printf("Base64 decoding failed!\n");
        return 1;
    }


    // Print decoded bytes for debugging
    printf("Decoded bytes (hex):\n");
    for (int i = 0; i < decoded_len; i++) {
        printf("%02x ", decoded[i]);
        if ((i + 1) % 16 == 0) printf("\n");
    }
    printf("\n");

    // Extract values from the decoded binary data
    int offset = 0;

    // Extract int
    memcpy(&int_, decoded + offset, sizeof(int));
    offset += sizeof(int);

    // Extract unsigned int
    memcpy(&uint_, decoded + offset, sizeof(unsigned int));
    offset += sizeof(unsigned int);

    // Extract short
    memcpy(&sint_, decoded + offset, sizeof(short));
    offset += sizeof(short)+2; // Add 2 to make sure the offset is 4 byte aligned

    // Extract float
    memcpy(&float_, decoded + offset, sizeof(float));
    offset += sizeof(float);

    // Extract double
    memcpy(&double_, decoded + offset, sizeof(double));
    offset += sizeof(double);

    // Extract big-endian double
    memcpy(&bigenddouble_, decoded + offset, sizeof(double));
    swap_bytes(&bigenddouble_, sizeof(double));  // Swap bytes for endianness

    // Print the unpacked values
    printf("int: %d\n", int_);
    printf("unsigned int: %u\n", uint_);
    printf("short: %d\n", sint_);
    printf("float: %f\n", float_);
    printf("double: %lf\n", double_);
    printf("big-endian double: %lf\n", bigenddouble_);

    // Debug: Print raw bytes of each extracted value
    printf("\nDebug: Raw bytes of extracted values:\n");
    printf("int bytes: ");
    for (size_t i = 0; i < sizeof(int); i++) {
        printf("%02x ", ((uint8_t*)&int_)[i]);
    }
    printf("\n");

    printf("unsigned int bytes: ");
    for (size_t i = 0; i < sizeof(unsigned int); i++) {
        printf("%02x ", ((uint8_t*)&uint_)[i]);
    }
    printf("\n");

    printf("short bytes: ");
    for (size_t i = 0; i < sizeof(short); i++) {
        printf("%02x ", ((uint8_t*)&sint_)[i]);
    }
    printf("\n");

    printf("float bytes: ");
    for (size_t i = 0; i < sizeof(float); i++) {
        printf("%02x ", ((uint8_t*)&float_)[i]);
    }
    printf("\n");

    printf("double bytes: ");
    for (size_t i = 0; i < sizeof(double); i++) {
        printf("%02x ", ((uint8_t*)&double_)[i]);
    }
    printf("\n");

    printf("big-endian double bytes: ");
    for (size_t i = 0; i < sizeof(double); i++) {
        printf("%02x ", ((uint8_t*)&bigenddouble_)[i]);
    }
    printf("\n");

    // Write the values to a JSON file
    FILE* fp = fopen("numbers.json", "w");
    if (fp == NULL) {
        printf("Failed to open file!\n");
        return 1;
    }

    fprintf(fp, "{\"int\":%d,\"uint\":%u,\"short\":%d,\"float\":%f,\"double\":%.15lf,\"big_endian_double\":%.15lf}",
        int_, uint_, sint_, float_, double_, bigenddouble_); // 15 decimal numbers because the verifier is precise
    fclose(fp);

    return 0;
}
