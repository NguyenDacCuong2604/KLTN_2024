package com.edu.nlu.document.service;

import com.edu.nlu.document.model.Department;

import java.util.List;

public interface DepartmentService {
    Department getDepartmentById(Long id);
    List<Department> getAllDepartments();
}
