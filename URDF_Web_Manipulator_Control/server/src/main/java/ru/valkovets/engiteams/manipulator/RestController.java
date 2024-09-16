package ru.valkovets.engiteams.manipulator;

import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;

import java.util.Collections;
import java.util.Map;

@Controller
@RequiredArgsConstructor
public class RestController {
private final ManipulatorService manipulatorService;

@GetMapping("/{partNumber}")
@ResponseBody
public Map<String, String> setPart(@PathVariable final int partNumber,
                                   @RequestParam final float angle) {
    final int partIndex = partNumber - 1;
    return Collections.singletonMap("state", manipulatorService.setState(partIndex, angle));
}

@GetMapping("/stop")
@ResponseBody
public Map<String, String> stop() {
    return Collections.singletonMap("state", manipulatorService.stop());
}

}
