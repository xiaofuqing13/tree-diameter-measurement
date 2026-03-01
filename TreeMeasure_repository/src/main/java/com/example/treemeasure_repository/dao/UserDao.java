package com.example.treemeasure_repository.dao;

import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface UserDao {
    public String userLogin(String username);
    public void userRegister(String username,String password);
}
