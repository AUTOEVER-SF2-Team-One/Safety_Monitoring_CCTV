package com.autoever.cctv;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.mybatis.spring.annotation.MapperScan;

@SpringBootApplication(scanBasePackages = "com.autoever")
@MapperScan("com.autoever.mapper")
public class CctvApplication {
    public static void main(String[] args) {
        SpringApplication.run(CctvApplication.class, args);
    }
}