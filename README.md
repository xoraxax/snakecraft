# Snakecraft: Generate Terraform code from Python

Have you ever felt writing Terraform code was very verbose? Have you ever disliked passing variables into layers of modules?

Snakecraft allows you to write your Terraform configuration in Python and generate the necessary Terraform code (as a `.tf.json` file).

Python 3.6 is required at least.

## Installing and running Snakecraft

You can install Snakecraft using `pip`:

```bash
pip install -U snakecraft
```

Afterwards, you can author Snakecraft modules/packages in Python code. If you want to
dive into Snakecraft by reading the [examples](https://github.com/xoraxax/snakecraft/tree/main/examples), you can clone them from Github
and process them using Snakecraft:

```bash
git clone https://github.com/xoraxax/snakecraft.git

cd snakecraft/examples

# The next commands reads snakecraft.ini:
snakecraft

# Now we can run Terraform:
cd simple_example
terraform init
terraform plan
```

As Snakecraft is still in an early stage, documentation is to be done.
