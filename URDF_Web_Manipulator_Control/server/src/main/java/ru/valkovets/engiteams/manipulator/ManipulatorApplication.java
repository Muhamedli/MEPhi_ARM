package ru.valkovets.engiteams.manipulator;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.web.servlet.config.annotation.EnableWebMvc;

@SpringBootApplication
@EnableWebMvc
public class ManipulatorApplication {

	public static void main(final String[] args) {
		SpringApplication.run(ManipulatorApplication.class, args);
	}

}
