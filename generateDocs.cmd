@echo off
pushd "Chat Server"
python -m pydoc -w chatServer
popd
pushd "Discovery Server"
python -m pydoc -w discoveryServer
popd
pushd "Client"
python -m pydoc -w client
popd