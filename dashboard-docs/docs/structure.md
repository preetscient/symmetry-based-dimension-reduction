## File Structure

```
├── LICENSE /
├── README.md \
├── dashboard-docs \
│   ├── docs \
│   ├── mkdocs.yml \
│   └── site \
├── data \
│   ├── external \
│   │   ├── 1_network_data \
│   │   │   └── networkrepository \
│   │   ├── 2_saucy_output \
│   │   │   └── networkrepository \
│   │   ├── 3_gap_readable_automorphism_data \
│   │   │   └── networkrepository \
│   │   ├── 4_network_data_csvs \
│   │   ├── 5_user_data \
│   │   │   └── reptilia-tortoise-network-sg.edges \
│   │   └── README.txt \
│   ├── interim \
│   │   ├── batch_gap_output \
│   │   ├── batch_lumping_output  \
│   │   │   ├── graph_data.csv \
│   │   │   ├── lumps_out.csv \
│   │   │   ├── orbit_colours \
│   │   │   ├── rowdat \
│   │   │   └── zaut_test \
│   │   ├── batch_processing_output \
│   │   ├── batch_saucy_output \
│   │   └── test_hash \
│   │       └── reptilia-tortoise-network-sg.edges \
│   ├── processed \
│   │   ├── gap_output \
│   │   │   └── reptilia-tortoise-network-sg.gap \
│   │   ├── lumping_output \
│   │   │   ├── lumps.csv \
│   │   │   ├── orbitcolours.txt \
│   │   │   ├── rowdat.json \
│   │   │   └── zaut_test.txt \
│   │   ├── processing_output \
│   │   │   ├── reptilia-tortoise-network-sg.scy \
│   │   │   └── source_target_view.csv \
│   │   ├── saucy_output \
│   │   │   └── reptilia-tortoise-network-sg.gaut \
│   │   └── viz_files \
│   └── raw \
│       └── reptilia-tortoise-network-sg.gap \
├── data_hash.json \
├── docs \
│   ├── commands.rst \
│   ├── conf.py \
│   ├── getting-started.rst \
│   ├── index.rst \
│   ├── make.bat \
│   └── mermaid_uml.md \
├── environment.yml \
├── file_structure.txt \
├── references \
├── saucy-3.0 \
├── setup_environment.bat \
├── setup_environment.sh \
├── skipped_networks.txt \
├── src \
│   ├── __init__.py \
│   ├── auts.py \
│   ├── batch_auts.py \
│   ├── batch_gaut2gap.py \
│   ├── batch_lumping.py \
│   ├── batch_processing.py \
│   ├── batch_run.py \
│   ├── config.py \
│   ├── gaut2gap.py \
│   ├── hashing.py \
│   ├── lumping.py \
│   ├── main.py \
│   ├── processing.py \
│   ├── trim.py \
│   ├── visualization \
│   │   ├── __init__.py \
│   │   ├── assets \
│   │   ├── visedges.csv \
│   │   └── viz_layout.py \
│   └── vizprocessing.py \
└── tests \
```

N.B. To generate this on macOS do: \
`brew install tree`  \
`tree --gitignore /path/to/symmetry-based-dimension-reduction > file_structure.txt`     

