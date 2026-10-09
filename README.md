# Jev Backstage Catalog Truth

## Français

**But.** Vérifier si une modification de fiche `Component` Backstage reste cohérente avec le motif annoncé et un extrait du README du service. Jev renvoie `consistent`, `contradiction` ou `review`. Un changement de propriétaire ou de cycle de vie impose toujours une revue humaine. Le programme ne modifie ni le catalogue ni les fichiers YAML.

**Entrée.** Deux fichiers `catalog-info.yaml` pour le même composant, un extrait de README et un motif. Le [format officiel Backstage](https://backstage.io/docs/next/features/software-catalog/descriptor-format/) définit `metadata.description`, `spec.type`, `spec.lifecycle` et `spec.owner`. Cette version accepte un seul document YAML `Component` par fichier. Les autres champs et les annotations ne partent pas vers Jev.

**Utilisation.** Installez `python3 -m pip install -r requirements.txt`, puis lancez `python3 app.py --demo`. Pour vos fichiers, chargez `TYPESAFE_API_KEY` dans l'environnement et lancez `python3 app.py --before ancien.yaml --after nouveau.yaml --readme extrait.txt --reason "Motif de la modification"`. Un dossier JSON avec `before_yaml`, `after_yaml`, `readme_excerpt` et `reason` fonctionne aussi via `--input`. Tests : `python3 -m unittest discover -s tests -v`. Le README est une preuve déclarative, pas une source de vérité absolue ; aucune publication de commentaire de PR n'est automatisée.

## English

**Purpose.** Check whether a Backstage `Component` descriptor change is consistent with the stated reason and a service README excerpt. Jev returns `consistent`, `contradiction`, or `review`. Owner or lifecycle changes always require human review. The tool modifies neither the catalog nor YAML files.

**Input.** Two `catalog-info.yaml` files for the same component, a README excerpt, and a reason. The [official Backstage format](https://backstage.io/docs/next/features/software-catalog/descriptor-format/) defines `metadata.description`, `spec.type`, `spec.lifecycle`, and `spec.owner`. This release accepts one `Component` YAML document per file. Other fields and annotations are excluded from Jev.

**Run.** Install `python3 -m pip install -r requirements.txt`, then run `python3 app.py --demo`. For your files, load `TYPESAFE_API_KEY` into the environment and run `python3 app.py --before old.yaml --after new.yaml --readme excerpt.txt --reason "Change reason"`. A JSON case with `before_yaml`, `after_yaml`, `readme_excerpt`, and `reason` also works through `--input`. Tests: `python3 -m unittest discover -s tests -v`. A README is declared evidence, not absolute truth; PR comments are not automated.

## Español

**Objetivo.** Comprobar si un cambio en una ficha `Component` de Backstage concuerda con el motivo declarado y un extracto del README del servicio. Jev devuelve `consistent`, `contradiction` o `review`. Los cambios de propietario o ciclo de vida siempre requieren revisión humana. La herramienta no modifica el catálogo ni los archivos YAML.

**Entrada.** Dos archivos `catalog-info.yaml` del mismo componente, un extracto del README y un motivo. El [formato oficial de Backstage](https://backstage.io/docs/next/features/software-catalog/descriptor-format/) define `metadata.description`, `spec.type`, `spec.lifecycle` y `spec.owner`. Esta versión acepta un único documento YAML `Component` por archivo. Los demás campos y anotaciones se excluyen de Jev.

**Uso.** Instale `python3 -m pip install -r requirements.txt` y ejecute `python3 app.py --demo`. Para sus archivos, cargue `TYPESAFE_API_KEY` en el entorno y ejecute `python3 app.py --before anterior.yaml --after nuevo.yaml --readme extracto.txt --reason "Motivo del cambio"`. También puede usar `--input` con un JSON que contenga `before_yaml`, `after_yaml`, `readme_excerpt` y `reason`. Pruebas: `python3 -m unittest discover -s tests -v`. El README es una prueba declarada, no una verdad absoluta; los comentarios de PR no se publican automáticamente.

MIT · v0.1.0
