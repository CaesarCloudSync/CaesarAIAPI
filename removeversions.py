new_rq = ""
with open("requirements_old.txt") as myFile:
  pkgs = myFile.read()
  pkgs = pkgs.splitlines()

  for pkg in pkgs:
      print(pkg.split('==')[0])
      new_rq += f"{pkg.split('==')[0]}\n"
with open("requirements.txt","w+") as myFile:
    myFile.write(new_rq)
