import subprocess
import tempfile
import unittest
from pathlib import Path


class SandpileTest(unittest.TestCase):
    def check_stability(self, grains):
        project = Path(__file__).resolve().parent
        code = r"""
#define main original_main
#include "main.cpp"
#undef main

int main(int argc, char* argv[]) {
    uint64_t grains = argv[1][0] - '0';
    uint64_t field[] = {0, 1, 2, grains};
    std::cout << IsStable(field, 2, 2);
    return 0;
}
"""
        with tempfile.TemporaryDirectory() as folder:
            source = Path(folder) / "test.cpp"
            program = Path(folder) / "test_program"
            source.write_text(code, encoding="utf-8") 
            subprocess.run(
                ["c++", "-std=c++17", "-Wno-return-type", "-I", str(project),
                str(source), "-o", str(program)],
                check=True,
                )
            result = subprocess.run(
                [str(program), str(grains)],
                capture_output=True, text=True, check=True,
                )
            return result.stdout.strip()
    def test_stable(self):
        self.assertEqual(self.check_stability(3), "1")

    def test_unstable(self):
        self.assertEqual(self.check_stability(4), "0")


    if __name__ == "__main__":
        unittest.main()
