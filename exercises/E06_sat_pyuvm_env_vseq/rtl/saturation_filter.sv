module saturation_filter #(
    parameter int IN_WIDTH  = 16,
    parameter int OUT_WIDTH = 8
) (
    input  logic                            clk,
    input  logic                            rst,
    input  logic                            in_valid,
    input  logic signed [IN_WIDTH-1:0]      in_data,
    output logic                            out_valid,
    output logic signed [OUT_WIDTH-1:0]     out_data
);

    localparam logic signed [IN_WIDTH-1:0] SAT_MAX =
        (2 ** (OUT_WIDTH - 1)) - 1;
    localparam logic signed [IN_WIDTH-1:0] SAT_MIN =
        -(2 ** (OUT_WIDTH - 1));

    initial begin
        if (OUT_WIDTH > IN_WIDTH)
            $error("OUT_WIDTH must be less than or equal to IN_WIDTH");
        if (OUT_WIDTH < 2)
            $error("OUT_WIDTH must be at least 2");
    end

    always_ff @(posedge clk) begin
        if (rst) begin
            out_valid <= 1'b0;
            out_data  <= '0;
        end else begin
            out_valid <= in_valid;

            if (in_valid) begin
                if ($signed(in_data) > SAT_MAX)
                    out_data <= SAT_MAX[OUT_WIDTH-1:0];
                else if ($signed(in_data) < SAT_MIN)
                    out_data <= SAT_MIN[OUT_WIDTH-1:0];
                else
                    out_data <= in_data[OUT_WIDTH-1:0];
            end
        end
    end

endmodule
