package com.edu.nlu.document.config;

import lombok.Getter;
import lombok.Setter;
import org.springframework.boot.context.properties.ConfigurationProperties;
import org.springframework.context.annotation.Configuration;

@Getter
@Setter
@Configuration
@ConfigurationProperties(prefix = "general")
public class GeneralProperties {
    // getters and setters
    private String externalApiUrl;
    private double thresholdMin;
    private double cutThreshold;
}
