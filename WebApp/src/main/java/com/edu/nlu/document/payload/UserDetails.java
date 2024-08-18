package com.edu.nlu.document.payload;

import com.edu.nlu.document.model.Department;
import com.edu.nlu.document.model.User;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonInclude;
import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

@Getter
@Setter
@ToString
@JsonIgnoreProperties(ignoreUnknown = true) // Bỏ qua các thuộc tính không được định nghĩa
@JsonInclude(JsonInclude.Include.NON_NULL) // Không bao gồm các thuộc tính null
public class UserDetails {
    private User user;
    private Department department;
    private double probability;
    private boolean isPredict;
    private boolean do_not_select;

}
