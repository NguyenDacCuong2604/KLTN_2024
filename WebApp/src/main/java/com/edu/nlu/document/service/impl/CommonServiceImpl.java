package com.edu.nlu.document.service.impl;

import com.edu.nlu.document.enums.Role;
import com.edu.nlu.document.model.User;
import com.edu.nlu.document.service.CommonService;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class CommonServiceImpl implements CommonService {
    private static final Long NO_LOGIN_USER_ID = -1L;

    public UserDetails getUserDetails() {
        return Optional.ofNullable(SecurityContextHolder.getContext().getAuthentication())
                .map(Authentication::getPrincipal)
                .filter(UserDetails.class::isInstance)
                .map(UserDetails.class::cast)
                .orElse(null);
    }

    @Override
    public Long getCurrentUserId() {
        return Optional.ofNullable(getUserDetails())
                .filter(userDetails -> userDetails instanceof User)
                .map(userDetails -> ((User) userDetails).getId())
                .orElse(NO_LOGIN_USER_ID);
    }

    @Override
    public Role getCurrentUserRole() {
        return Role.valueOf(getUserDetails().getAuthorities().stream().findFirst().get().getAuthority());
    }
}
