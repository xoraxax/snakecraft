variable "service" {}


resource "aws_iam_role" "role" {
  name = "test-role"

  assume_role_policy = <<EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
        "Effect": "Allow",
        "Principal": {
            "Service": ${var.service}
        },
        "Action": "sts:AssumeRole"
        }
    ]
}
EOF
}

output "test_output" {
  value = aws_iam_role.role.id
}


