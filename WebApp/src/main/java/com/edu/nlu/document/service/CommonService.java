package com.edu.nlu.document.service;

import com.edu.nlu.document.enums.Role;
import org.springframework.security.core.userdetails.UserDetails;

public interface CommonService {
    UserDetails getUserDetails();

    Long getCurrentUserId();

    Role getCurrentUserRole();


}
