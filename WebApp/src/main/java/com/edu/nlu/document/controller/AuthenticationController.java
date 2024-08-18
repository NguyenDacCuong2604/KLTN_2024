package com.edu.nlu.document.controller;

import com.edu.nlu.document.payload.LoginForm;
import com.edu.nlu.document.service.AuthenticationService;
import com.edu.nlu.document.service.DocumentService;
import lombok.RequiredArgsConstructor;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;

@RequiredArgsConstructor
@Controller
@RequestMapping(path = "/auth/v1")
public class AuthenticationController {

    @GetMapping(path = "/login")
    public String showLoginForm(Model model) {
        model.addAttribute("loginForm", new LoginForm());
        return "login";
    }
}
