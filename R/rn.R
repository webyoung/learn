name: Run R script

on: 
  push:
  #schedule: 
  #  - cron: '0 * * * *'

jobs:
  render:
    name: Run R script
    runs-on: macOS-latest
    steps:
      - uses: actions/checkout@v1
      - uses: r-lib/actions/setup-r@v1
      - uses: r-lib/actions/setup-pandoc@v1
      - name: Install packages
        run: Rscript R/install.R
      - name: Run R script
        run: Rscript R/rn.R
      - name: Commit results
        run: |
          git commit data.csv --allow-empty -m 'gHA build: ${{github.run_number}}' || echo "No changes to commit"
          git push https://${{github.actor}}:${{secrets.token}}@github.com/${{github.repository}}.git HEAD:${{ github.ref }} || echo "No changes "
