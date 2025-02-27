#include <stdio.h>
#include <stdlib.h>
#include "bbb_mmio.h"
#include "bbb_dht_read.h"

#define DHT11_TYPE 11  // Tipo de sensor: 11 para DHT11

int main(void) {
    // Para o GPIO 48, usamos:
    // Banco: 1
    // Número: 16 (pois 48 = 1*32 + 16)
    int gpio_base = 1;
    int gpio_number = 16;
    float temperatura, umidade;
    
    printf("Iniciando leitura do sensor DHT11...\n");
    
    if (bbb_dht_read(DHT11_TYPE, gpio_base, gpio_number, &umidade, &temperatura) == 0) {
        printf("Leitura bem-sucedida!\n");
        printf("Temperatura: %.1f°C\n", temperatura);
        printf("Umidade: %.1f%%\n", umidade);
    } else {
        printf("Erro ao ler o sensor DHT11!\n");
    }
    
    return 0;
}

