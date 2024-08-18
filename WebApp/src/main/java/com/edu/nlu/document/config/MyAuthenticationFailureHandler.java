package com.edu.nlu.document.config;

import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.context.annotation.Primary;
import org.springframework.security.core.AuthenticationException;
import org.springframework.security.web.authentication.AuthenticationFailureHandler;
import org.springframework.stereotype.Component;

import java.io.IOException;
@Slf4j
@RequiredArgsConstructor
@Component
@Primary
public class MyAuthenticationFailureHandler implements AuthenticationFailureHandler {
    @Override
    public void onAuthenticationFailure(HttpServletRequest request, HttpServletResponse response, AuthenticationException exception) throws IOException {
        // Custom logic on failure, like logging or setting error messages
        log.info("Authentication failure");
        request.getSession().setAttribute("error", "Login failed: " + exception.getMessage());

        response.sendRedirect(request.getContextPath() + "/auth/v1/login?error");
    }
}
