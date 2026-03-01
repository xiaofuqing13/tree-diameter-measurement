package com.example.treemeasure_repository.controller;

import com.example.treemeasure_repository.dao.UserDao;
import com.example.treemeasure_repository.entity.ReturnMessage;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class UserController {
    @Autowired
    UserDao userDao;
    @RequestMapping("/userLogin")
    public ReturnMessage userLogin(String username,String password){
        String passwordData=userDao.userLogin(username);
        ReturnMessage returnMessage=new ReturnMessage();
        if(password.equals(passwordData))
        {
            returnMessage.setCode("200");
            returnMessage.setMessage(("success"));
        }
        else {
            returnMessage.setCode("500");
            returnMessage.setMessage(("failed"));
        }
        return returnMessage;
    }

    @RequestMapping("/userRegister")
    public ReturnMessage userRegister(String username,String password){
        ReturnMessage returnMessage=new ReturnMessage();
        try {
            userDao.userRegister(username,password);
            returnMessage.setCode("200");
            returnMessage.setMessage(("success"));
        }catch (Exception e){
            returnMessage.setCode("500");
            returnMessage.setMessage(("failed"));
        }
        return returnMessage;
    }
}
