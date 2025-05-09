hyperfine -w 3 -r 15 "python test_inputs.py demo | python demo/zero.py"
hyperfine -w 3 -r 15 "python test_inputs.py demo | python demo/zero_pa_qe.py"

hyperfine -w 3 -r 15 "python test_inputs.py demo | python demo/five.py"
hyperfine -w 3 -r 15 "python test_inputs.py demo | python demo/five_pa_qe.py"

hyperfine -w 3 -r 15 "python test_inputs.py demo | python demo/ten.py"
hyperfine -w 3 -r 15 "python test_inputs.py demo | python demo/ten_pa_qe.py"
