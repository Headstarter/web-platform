export DEBUG=on;
export CONFIG=config.cfg;
bash ssh/.ssh/gen.sh | xargs -I{} sed -E 's/({})//g' ssh/.ssh/migration07082019.py | python