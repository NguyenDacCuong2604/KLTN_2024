package com.edu.nlu.document.repository;

import com.edu.nlu.document.enums.Role;
import com.edu.nlu.document.model.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.Optional;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {

    boolean existsByUsernameAndPassword(String username, String password);

    Optional<User> findByUsername(String username);

    List<User> findAllByRole(String role);
    List<User> findAllByDepartmentId(Long departmentId);

}
