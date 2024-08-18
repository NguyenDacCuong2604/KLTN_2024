package com.edu.nlu.document.service.impl;

import com.edu.nlu.document.model.Department;
import com.edu.nlu.document.repository.DepartmentRepository;
import com.edu.nlu.document.service.DepartmentService;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class DeparmentServiceImpl implements DepartmentService {
    private final DepartmentRepository departmentRepository;

    @Override
    public Department getDepartmentById(Long id) {
        return departmentRepository.getReferenceById(id);
    }

    @Override
    public List<Department> getAllDepartments() {
        return departmentRepository.findByHostIdIsNotNull();
    }


}
