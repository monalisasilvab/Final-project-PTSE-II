#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "bbb_mmio.h"
#include "bbb_dht_read.h"

#define DHT11_TYPE 11  // Tipo de sensor: 11 para DHT11
#define CSV_FILE "historico.csv"

void salvar_historico(float temperatura, float umidade) {
    FILE *file = fopen(CSV_FILE, "a");
    if (file == NULL) {
        perror("Erro ao abrir arquivo CSV");
        return;
    }
    
    time_t t = time(NULL);
    struct tm tm = *localtime(&t);
    
    fprintf(file, "%04d-%02d-%02d %02d:%02d:%02d,%.1f,%.1f\n",
            tm.tm_year + 1900, tm.tm_mon + 1, tm.tm_mday,
            tm.tm_hour, tm.tm_min, tm.tm_sec,
            temperatura, umidade);
    fclose(file);
}

int main(void) {
    int gpio_base = 1;
    int gpio_number = 16;
    float temperatura, umidade;
    
    printf("Iniciando leitura do sensor DHT11...\n");
    
    if (bbb_dht_read(DHT11_TYPE, gpio_base, gpio_number, &umidade, &temperatura) == 0) {
        printf("Leitura bem-sucedida!\n");
        printf("Temperatura: %.1f°C\n", temperatura);
        printf("Umidade: %.1f%%\n", umidade);
        salvar_historico(temperatura, umidade);
    } else {
        printf("Erro ao ler o sensor DHT11!\n");
    }
    
    return 0;
}

