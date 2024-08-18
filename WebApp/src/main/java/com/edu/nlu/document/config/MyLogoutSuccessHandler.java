package com.edu.nlu.document.config;

import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.context.annotation.Primary;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.web.authentication.logout.LogoutSuccessHandler;
import org.springframework.stereotype.Component;

import java.io.IOException;

@Slf4j
@RequiredArgsConstructor
@Component
@Primary
public class MyLogoutSuccessHandler implements LogoutSuccessHandler {
    @Override
    public void onLogoutSuccess(HttpServletRequest request, HttpServletResponse response, Authentication authentication) throws IOException, ServletException {
        log.info("User logged out successfully.");
        if (request.getSession() != null) {
            // Optionally, remove specific attributes
            request.getSession().removeAttribute("specificAttribute");
            request.getSession().invalidate();
        }
        SecurityContextHolder.clearContext();
        // Redirect to the login page with a logout parameter
        response.sendRedirect(request.getContextPath() + "/auth/v1/login?logout");
    }
}
