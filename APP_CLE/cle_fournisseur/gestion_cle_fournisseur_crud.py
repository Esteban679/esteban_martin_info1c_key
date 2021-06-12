"""
    Fichier : gestion_films_genres_crud.py
    Auteur : OM 2021.05.01
    Gestions des "routes" FLASK et des données pour l'association entre les films et les genres.
"""
import sys

import pymysql
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for

from APP_CLE import obj_mon_application
from APP_CLE.database.connect_db_context_manager import MaBaseDeDonnee
from APP_CLE.erreurs.exceptions import *
from APP_CLE.erreurs.msg_erreurs import *
from APP_CLE.cle_fournisseur.gestion_fournisseur_c_wtf_forms import FormWTFAjouterGenres
from APP_CLE.cle_fournisseur.gestion_fournisseur_c_wtf_forms import FormWTFUpdateGenre
from APP_CLE.cle_fournisseur.gestion_fournisseur_c_wtf_forms import FormWTFDeleteGenre


"""
    Nom : films_genres_afficher
    Auteur : OM 2021.05.01
    Définition d'une "route" /films_genres_afficher
    
    But : Afficher les films avec les genres associés pour chaque film.
    
    Paramètres : id_genre_sel = 0 >> tous les films.
                 id_genre_sel = "n" affiche le film dont l'id est "n"
                 
"""


@obj_mon_application.route("/cle_fournisseur_afficher/<int:id_cle_sel>", methods=['GET', 'POST'])
def cle_fournisseur_afficher(id_cle_sel):
    if request.method == "GET":
        try:
            try:
                # Renvoie une erreur si la connexion est perdue.
                MaBaseDeDonnee().connexion_bd.ping(False)
            except Exception as Exception_init_films_genres_afficher:
                code, msg = Exception_init_films_genres_afficher.args
                flash(f"{error_codes.get(code, msg)} ", "danger")
                flash(f"Exception _init_films_genres_afficher problème de connexion BD : {sys.exc_info()[0]} "
                      f"{Exception_init_films_genres_afficher.args[0]} , "
                      f"{Exception_init_films_genres_afficher}", "danger")
                raise MaBdErreurConnexion(f"{msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[0]}")

            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                strsql_genres_films_afficher_data = """SELECT id_cle, nom_cle, couleur,
                                                            GROUP_CONCAT(' ',nom_fournisseur) as GenresFilms FROM t_avoir_fournisseur
                                                            RIGHT JOIN t_cle ON t_cle.id_cle = t_avoir_fournisseur.fk_cle
                                                            LEFT JOIN t_fournisseur ON t_fournisseur.id_fournisseur = t_avoir_fournisseur.fk_fournisseur
                                                            GROUP BY id_cle"""
                if id_cle_sel == 0:
                    # le paramètre 0 permet d'afficher tous les films
                    # Sinon le paramètre représente la valeur de l'id du film
                    mc_afficher.execute(strsql_genres_films_afficher_data)
                else:
                    # Constitution d'un dictionnaire pour associer l'id du film sélectionné avec un nom de variable
                    valeur_id_film_selected_dictionnaire = {"value_id_cle_selected": id_cle_sel}
                    # En MySql l'instruction HAVING fonctionne comme un WHERE... mais doit être associée à un GROUP BY
                    # L'opérateur += permet de concaténer une nouvelle valeur à la valeur de gauche préalablement définie.
                    strsql_genres_films_afficher_data += """ HAVING id_cle= %(value_id_cle_selected)s"""

                    mc_afficher.execute(strsql_genres_films_afficher_data, valeur_id_film_selected_dictionnaire)

                # Récupère les données de la requête.
                data_genres_films_afficher = mc_afficher.fetchall()
                print("data_fournisseur ", data_genres_films_afficher, " Type : ", type(data_genres_films_afficher))

                # Différencier les messages.
                if not data_genres_films_afficher and id_cle_sel == 0:
                    flash("""La table "t_cle" est vide. !""", "warning")
                elif not data_genres_films_afficher and id_cle_sel > 0:
                    # Si l'utilisateur change l'id_film dans l'URL et qu'il ne correspond à aucun film
                    flash(f"La clé {id_cle_sel} demandé n'existe pas !!", "warning")
                else:
                    flash(f"Données clés et fournisseur affichés !!", "success")

        except Exception as Exception_films_genres_afficher:
            code, msg = Exception_films_genres_afficher.args
            flash(f"{error_codes.get(code, msg)} ", "danger")
            flash(f"Exception films_genres_afficher : {sys.exc_info()[0]} "
                  f"{Exception_films_genres_afficher.args[0]} , "
                  f"{Exception_films_genres_afficher}", "danger")

    # Envoie la page "HTML" au serveur.
    return render_template("cle_fournisseur/cle_fournisseur_afficher.html", data=data_genres_films_afficher)


"""
    nom: edit_genre_film_selected
    On obtient un objet "objet_dumpbd"

    Récupère la liste de tous les genres du film sélectionné par le bouton "MODIFIER" de "films_genres_afficher.html"
    
    Dans une liste déroulante particulière (tags-selector-tagselect), on voit :
    1) Tous les genres contenus dans la "t_genre".
    2) Les genres attribués au film selectionné.
    3) Les genres non-attribués au film sélectionné.

    On signale les erreurs importantes

"""


@obj_mon_application.route("/edit_genre_film_selected", methods=['GET', 'POST'])
def edit_genre_film_selected():
    if request.method == "GET":
        try:
            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                strsql_genres_afficher = """SELECT id_fournisseur, nom_fournisseur FROM t_fournisseur ORDER BY id_fournisseur ASC"""
                mc_afficher.execute(strsql_genres_afficher)
            data_genres_all = mc_afficher.fetchall()
            print("dans edit_genre_film_selected ---> data_genres_all", data_genres_all)

            # Récupère la valeur de "id_film" du formulaire html "films_genres_afficher.html"
            # l'utilisateur clique sur le bouton "Modifier" et on récupère la valeur de "id_film"
            # grâce à la variable "id_film_genres_edit_html" dans le fichier "films_genres_afficher.html"
            # href="{{ url_for('edit_genre_film_selected', id_film_genres_edit_html=row.id_film) }}"
            id_film_genres_edit = request.values['id_film_genres_edit_html']

            # Mémorise l'id du film dans une variable de session
            # (ici la sécurité de l'application n'est pas engagée)
            # il faut éviter de stocker des données sensibles dans des variables de sessions.
            session['session_id_film_genres_edit'] = id_film_genres_edit

            # Constitution d'un dictionnaire pour associer l'id du film sélectionné avec un nom de variable
            valeur_id_cle_selected_dictionnaire = {"value_id_cle_selected": id_film_genres_edit}

            # Récupère les données grâce à 3 requêtes MySql définie dans la fonction genres_films_afficher_data
            # 1) Sélection du film choisi
            # 2) Sélection des genres "déjà" attribués pour le film.
            # 3) Sélection des genres "pas encore" attribués pour le film choisi.
            # ATTENTION à l'ordre d'assignation des variables retournées par la fonction "genres_films_afficher_data"
            data_genre_film_selected, data_genres_films_non_attribues, data_genres_films_attribues = \
                genres_films_afficher_data(valeur_id_cle_selected_dictionnaire)

            print(data_genre_film_selected)
            lst_data_film_selected = [item['id_cle'] for item in data_genre_film_selected]
            print("lst_data_film_selected  ", lst_data_film_selected,
                  type(lst_data_film_selected))

            # Dans le composant "tags-selector-tagselect" on doit connaître
            # les genres qui ne sont pas encore sélectionnés.
            lst_data_genres_films_non_attribues = [item['id_fournisseur'] for item in data_genres_films_non_attribues]
            session['session_lst_data_genres_films_non_attribues'] = lst_data_genres_films_non_attribues
            print("lst_data_genres_films_non_attribues  ", lst_data_genres_films_non_attribues,
                  type(lst_data_genres_films_non_attribues))

            # Dans le composant "tags-selector-tagselect" on doit connaître
            # les genres qui sont déjà sélectionnés.
            lst_data_genres_films_old_attribues = [item['id_fournisseur'] for item in data_genres_films_attribues]
            session['session_lst_data_genres_films_old_attribues'] = lst_data_genres_films_old_attribues
            print("lst_data_genres_films_old_attribues  ", lst_data_genres_films_old_attribues,
                  type(lst_data_genres_films_old_attribues))

            print(" data data_genre_film_selected", data_genre_film_selected, "type ", type(data_genre_film_selected))
            print(" data data_genres_films_non_attribues ", data_genres_films_non_attribues, "type ",
                  type(data_genres_films_non_attribues))
            print(" data_genres_films_attribues ", data_genres_films_attribues, "type ",
                  type(data_genres_films_attribues))

            # Extrait les valeurs contenues dans la table "t_genres", colonne "intitule_genre"
            # Le composant javascript "tagify" pour afficher les tags n'a pas besoin de l'id_genre
            lst_data_genres_films_non_attribues = [item['nom_fournisseur'] for item in data_genres_films_non_attribues]
            print("lst_all_genres gf_edit_genre_film_selected ", lst_data_genres_films_non_attribues,
                  type(lst_data_genres_films_non_attribues))

        except Exception as Exception_edit_genre_film_selected:
            code, msg = Exception_edit_genre_film_selected.args
            flash(f"{error_codes.get(code, msg)} ", "danger")
            flash(f"Exception edit_genre_film_selected : {sys.exc_info()[0]} "
                  f"{Exception_edit_genre_film_selected.args[0]} , "
                  f"{Exception_edit_genre_film_selected}", "danger")

    return render_template("cle_fournisseur/films_genres_modifier_tags_dropbox.html",
                           data_genres=data_genres_all,
                           data_film_selected=data_genre_film_selected,
                           data_genres_attribues=data_genres_films_attribues,
                           data_genres_non_attribues=data_genres_films_non_attribues)


"""
    nom: update_genre_film_selected

    Récupère la liste de tous les genres du film sélectionné par le bouton "MODIFIER" de "films_genres_afficher.html"
    
    Dans une liste déroulante particulière (tags-selector-tagselect), on voit :
    1) Tous les genres contenus dans la "t_genre".
    2) Les genres attribués au film selectionné.
    3) Les genres non-attribués au film sélectionné.

    On signale les erreurs importantes
"""


@obj_mon_application.route("/update_genre_film_selected", methods=['GET', 'POST'])
def update_genre_film_selected():
    if request.method == "POST":
        try:
            # Récupère l'id du film sélectionné
            id_cle_selected = session['session_id_film_genres_edit']
            print("session['session_id_film_genres_edit'] ", session['session_id_film_genres_edit'])

            # Récupère la liste des genres qui ne sont pas associés au film sélectionné.
            old_lst_data_genres_films_non_attribues = session['session_lst_data_genres_films_non_attribues']
            print("old_lst_data_genres_films_non_attribues ", old_lst_data_genres_films_non_attribues)

            # Récupère la liste des genres qui sont associés au film sélectionné.
            old_lst_data_genres_films_attribues = session['session_lst_data_genres_films_old_attribues']
            print("old_lst_data_genres_films_old_attribues ", old_lst_data_genres_films_attribues)

            # Effacer toutes les variables de session.
            session.clear()

            # Récupère ce que l'utilisateur veut modifier comme genres dans le composant "tags-selector-tagselect"
            # dans le fichier "genres_films_modifier_tags_dropbox.html"
            new_lst_str_genres_films = request.form.getlist('name_select_tags')
            print("new_lst_str_genres_films ", new_lst_str_genres_films)

            # OM 2021.05.02 Exemple : Dans "name_select_tags" il y a ['4','65','2']
            # On transforme en une liste de valeurs numériques. [4,65,2]
            new_lst_int_genre_film_old = list(map(int, new_lst_str_genres_films))
            print("new_lst_genre_film ", new_lst_int_genre_film_old, "type new_lst_genre_film ",
                  type(new_lst_int_genre_film_old))

            # Pour apprécier la facilité de la vie en Python... "les ensembles en Python"
            # https://fr.wikibooks.org/wiki/Programmation_Python/Ensembles
            # OM 2021.05.02 Une liste de "id_genre" qui doivent être effacés de la table intermédiaire "t_genre_film".
            lst_diff_genres_delete_b = list(
                set(old_lst_data_genres_films_attribues) - set(new_lst_int_genre_film_old))
            print("lst_diff_genres_delete_b ", lst_diff_genres_delete_b)

            # Une liste de "id_genre" qui doivent être ajoutés à la "t_genre_film"
            lst_diff_genres_insert_a = list(
                set(new_lst_int_genre_film_old) - set(old_lst_data_genres_films_attribues))
            print("lst_diff_genres_insert_a ", lst_diff_genres_insert_a)

            # SQL pour insérer une nouvelle association entre
            # "fk_film"/"id_film" et "fk_genre"/"id_genre" dans la "t_genre_film"
            strsql_insert_genre_film = """INSERT INTO t_avoir_fournisseur (id_avoir_fournisseur, fk_fournisseur, fk_cle)
                                                    VALUES (NULL, %(value_fk_fournisseur)s, %(value_fk_cle)s)"""

            # SQL pour effacer une (des) association(s) existantes entre "id_film" et "id_genre" dans la "t_genre_film"
            strsql_delete_genre_film = """DELETE FROM t_avoir_fournisseur WHERE fk_fournisseur = %(value_fk_fournisseur)s AND fk_cle = %(value_fk_cle)s"""

            with MaBaseDeDonnee() as mconn_bd:
                # Pour le film sélectionné, parcourir la liste des genres à INSÉRER dans la "t_genre_film".
                # Si la liste est vide, la boucle n'est pas parcourue.
                for id_fournisseur_ins in lst_diff_genres_insert_a:
                    # Constitution d'un dictionnaire pour associer l'id du film sélectionné avec un nom de variable
                    # et "id_fournisseur_ins" (l'id du genre dans la liste) associé à une variable.
                    valeurs_film_sel_genre_sel_dictionnaire = {"value_fk_cle": id_cle_selected,
                                                               "value_fk_fournisseur": id_fournisseur_ins}

                    mconn_bd.mabd_execute(strsql_insert_genre_film, valeurs_film_sel_genre_sel_dictionnaire)

                # Pour le film sélectionné, parcourir la liste des genres à EFFACER dans la "t_genre_film".
                # Si la liste est vide, la boucle n'est pas parcourue.
                for id_fournisseur_del in lst_diff_genres_delete_b:
                    # Constitution d'un dictionnaire pour associer l'id du film sélectionné avec un nom de variable
                    # et "id_genre_del" (l'id du genre dans la liste) associé à une variable.
                    valeurs_film_sel_genre_sel_dictionnaire = {"value_fk_cle": id_cle_selected,
                                                               "value_fk_fournisseur": id_fournisseur_del}

                    # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
                    # la subtilité consiste à avoir une méthode "mabd_execute" dans la classe "MaBaseDeDonnee"
                    # ainsi quand elle aura terminé l'insertion des données le destructeur de la classe "MaBaseDeDonnee"
                    # sera interprété, ainsi on fera automatiquement un commit
                    mconn_bd.mabd_execute(strsql_delete_genre_film, valeurs_film_sel_genre_sel_dictionnaire)

        except Exception as Exception_update_genre_film_selected:
            code, msg = Exception_update_genre_film_selected.args
            flash(f"{error_codes.get(code, msg)} ", "danger")
            flash(f"Exception update_genre_film_selected : {sys.exc_info()[0]} "
                  f"{Exception_update_genre_film_selected.args[0]} , "
                  f"{Exception_update_genre_film_selected}", "danger")

    # Après cette mise à jour de la table intermédiaire "t_genre_film",
    # on affiche les films et le(urs) genre(s) associé(s).
    return redirect(url_for('cle_fournisseur_afficher', id_cle_sel=id_cle_selected))


"""
    nom: genres_films_afficher_data

    Récupère la liste de tous les genres du film sélectionné par le bouton "MODIFIER" de "films_genres_afficher.html"
    Nécessaire pour afficher tous les "TAGS" des genres, ainsi l'utilisateur voit les genres à disposition

    On signale les erreurs importantes
"""


def genres_films_afficher_data(valeur_id_cle_selected_dict):
    print("valeur_id_cle_selected_dict...", valeur_id_cle_selected_dict)
    try:

        strsql_film_selected = """SELECT id_cle, nom_cle, couleur, GROUP_CONCAT(id_fournisseur) as GenresFilms FROM t_avoir_fournisseur
                                        INNER JOIN t_cle ON t_cle.id_cle = t_avoir_fournisseur.fk_cle
                                        INNER JOIN t_fournisseur ON t_fournisseur.id_fournisseur = t_avoir_fournisseur.fk_fournisseur
                                        WHERE id_cle = %(value_id_cle_selected)s"""

        strsql_genres_films_non_attribues = """SELECT id_fournisseur, nom_fournisseur FROM t_fournisseur WHERE id_fournisseur not in(SELECT id_fournisseur as idGenresFilms FROM t_avoir_fournisseur
                                                    INNER JOIN t_cle ON t_cle.id_cle = t_avoir_fournisseur.fk_cle
                                                    INNER JOIN t_fournisseur ON t_fournisseur.id_fournisseur = t_avoir_fournisseur.fk_fournisseur
                                                    WHERE id_cle = %(value_id_cle_selected)s)"""

        strsql_genres_films_attribues = """SELECT id_cle, id_fournisseur, nom_fournisseur FROM t_avoir_fournisseur
                                            INNER JOIN t_cle ON t_cle.id_cle = t_avoir_fournisseur.fk_cle
                                            INNER JOIN t_fournisseur ON t_fournisseur.id_fournisseur = t_avoir_fournisseur.fk_fournisseur
                                            WHERE id_cle = %(value_id_cle_selected)s"""

        # Du fait de l'utilisation des "context managers" on accède au curseur grâce au "with".
        with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
            # Envoi de la commande MySql
            mc_afficher.execute(strsql_genres_films_non_attribues, valeur_id_cle_selected_dict)
            # Récupère les données de la requête.
            data_genres_films_non_attribues = mc_afficher.fetchall()
            # Affichage dans la console
            print("genres_films_afficher_data ----> data_genres_films_non_attribues ", data_genres_films_non_attribues,
                  " Type : ",
                  type(data_genres_films_non_attribues))

            # Envoi de la commande MySql
            mc_afficher.execute(strsql_film_selected, valeur_id_cle_selected_dict)
            # Récupère les données de la requête.
            data_film_selected = mc_afficher.fetchall()
            # Affichage dans la console
            print("data_film_selected  ", data_film_selected, " Type : ", type(data_film_selected))

            # Envoi de la commande MySql
            mc_afficher.execute(strsql_genres_films_attribues, valeur_id_cle_selected_dict)
            # Récupère les données de la requête.
            data_genres_films_attribues = mc_afficher.fetchall()
            # Affichage dans la console
            print("data_genres_films_attribues ", data_genres_films_attribues, " Type : ",
                  type(data_genres_films_attribues))

            # Retourne les données des "SELECT"
            return data_film_selected, data_genres_films_non_attribues, data_genres_films_attribues
    except pymysql.Error as pymysql_erreur:
        code, msg = pymysql_erreur.args
        flash(f"{error_codes.get(code, msg)} ", "danger")
        flash(f"pymysql.Error Erreur dans genres_films_afficher_data : {sys.exc_info()[0]} "
              f"{pymysql_erreur.args[0]} , "
              f"{pymysql_erreur}", "danger")
    except Exception as exception_erreur:
        code, msg = exception_erreur.args
        flash(f"{error_codes.get(code, msg)} ", "danger")
        flash(f"Exception Erreur dans genres_films_afficher_data : {sys.exc_info()[0]} "
              f"{exception_erreur.args[0]} , "
              f"{exception_erreur}", "danger")
    except pymysql.err.IntegrityError as IntegrityError_genres_films_afficher_data:
        code, msg = IntegrityError_genres_films_afficher_data.args
        flash(f"{error_codes.get(code, msg)} ", "danger")
        flash(f"pymysql.err.IntegrityError Erreur dans genres_films_afficher_data : {sys.exc_info()[0]} "
              f"{IntegrityError_genres_films_afficher_data.args[0]} , "
              f"{IntegrityError_genres_films_afficher_data}", "danger")


"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /genres_ajouter

    Test : ex : http://127.0.0.1:5005/genres_ajouter

    Paramètres : sans

    But : Ajouter un genre pour un film

    Remarque :  Dans le champ "name_genre_html" du formulaire "genres/genres_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@obj_mon_application.route("/cle_ajouter", methods=['GET', 'POST'])
def cle_ajouter_wtf():
    form = FormWTFAjouterGenres()
    if request.method == "POST":
        try:
            try:
                # Renvoie une erreur si la connexion est perdue.
                MaBaseDeDonnee().connexion_bd.ping(False)
            except Exception as erreur:
                flash(f"Dans Gestion genres ...terrible erreur, il faut connecter une base de donnée", "danger")
                print(f"Exception grave Classe constructeur GestionGenres {erreur.args[0]}")
                raise MaBdErreurConnexion(f"{msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[0]}")

            if form.validate_on_submit():
                name_nom_fournisseur_wtf = form.nom_nom_fournisseur_wtf.data

                name_nom_fournisseur = name_nom_fournisseur_wtf.capitalize()

                name_nom_couleur_wtf = form.nom_nom_couleur_wtf.data
                name_nom_couleur = name_nom_couleur_wtf.capitalize()
                valeurs_insertion_dictionnaire = {"value_nom_cle": name_nom_fournisseur,
                                                  "value_couleur": name_nom_couleur}
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_nom_fournisseur = """INSERT INTO t_cle (id_cle,nom_cle, couleur) VALUES (NULL,%(value_nom_cle)s, %(value_couleur)s)"""
                with MaBaseDeDonnee() as mconn_bd:
                    mconn_bd.mabd_execute(strsql_insert_nom_fournisseur, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('cle_fournisseur_afficher', order_by='DESC', id_cle_sel=0))

        # ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
        except pymysql.err.IntegrityError as erreur_nom_fournisseur_doublon:
            # Dérive "pymysql.err.IntegrityError" dans "MaBdErreurDoublon" fichier "erreurs/exceptions.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            code, msg = erreur_nom_fournisseur_doublon.args

            flash(f"{error_codes.get(code, msg)} ", "warning")

        # OM 2020.04.16 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
        except (pymysql.err.OperationalError,
                pymysql.ProgrammingError,
                pymysql.InternalError,
                TypeError) as erreur_gest_genr_crud:
            code, msg = erreur_gest_genr_crud.args

            flash(f"{error_codes.get(code, msg)} ", "danger")
            flash(f"Erreur dans Gestion genres CRUD : {sys.exc_info()[0]} "
                  f"{erreur_gest_genr_crud.args[0]} , "
                  f"{erreur_gest_genr_crud}", "danger")

    return render_template("cles/cle_ajouter_wtf.html", form=form)


"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /genre_update

    Test : ex cliquer sur le menu "genres" puis cliquer sur le bouton "EDIT" d'un "genre"

    Paramètres : sans

    But : Editer(update) un genre qui a été sélectionné dans le formulaire "genres_afficher.html"

    Remarque :  Dans le champ "nom_genre_update_wtf" du formulaire "genres/genre_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@obj_mon_application.route("/cle_update", methods=['GET', 'POST'])
def cle_update_wtf():
    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_genre"
    id_cle_update = request.values['id_genre_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdateGenre()
    try:
        print(" on submit ", form_update.validate_on_submit())
        if form_update.validate_on_submit():
            # Récupèrer la valeur du champ depuis "genre_update_wtf.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            name_genre_update = form_update.nom_genre_update_wtf.data
            name_genre_update = name_genre_update.capitalize()

            value_couleur = form_update.couleur_update_wtf.data
            value_couleur = value_couleur.capitalize()

            valeur_update_dictionnaire = {"value_id_cle": id_cle_update, "value_name_fournisseur": name_genre_update,
                                          "value_couleur": value_couleur}
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_intitulegenre = """UPDATE t_cle SET nom_cle = %(value_name_fournisseur)s, couleur = %(value_couleur)s WHERE id_cle = %(value_id_cle)s"""
            with MaBaseDeDonnee() as mconn_bd:
                mconn_bd.mabd_execute(str_sql_update_intitulegenre, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_genre_update"
            return redirect(url_for('cle_fournisseur_afficher', order_by="ASC", id_cle_sel=id_cle_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_genre" et "intitule_genre" de la "t_genre"
            str_sql_id_genre = "SELECT id_cle, nom_cle, couleur FROM t_cle WHERE id_cle = %(value_id_cle)s"
            valeur_select_dictionnaire = {"value_id_cle": id_cle_update}
            mybd_curseur = MaBaseDeDonnee().connexion_bd.cursor()
            mybd_curseur.execute(str_sql_id_genre, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom genre" pour l'UPDATE
            data_nom_fournisseur = mybd_curseur.fetchone()
            print("data_nom_fournisseur ", data_nom_fournisseur, " type ", type(data_nom_fournisseur), " genre ",
                  data_nom_fournisseur["nom_cle"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "genre_update_wtf.html"
            form_update.nom_genre_update_wtf.data = data_nom_fournisseur["nom_cle"]
            form_update.couleur_update_wtf.data = data_nom_fournisseur["couleur"]

    # OM 2020.04.16 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
    except KeyError:
        flash(f"__KeyError dans genre_update_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")
    except ValueError:
        flash(f"Erreur dans genre_update_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]}", "danger")
    except (pymysql.err.OperationalError,
            pymysql.ProgrammingError,
            pymysql.InternalError,
            pymysql.err.IntegrityError,
            TypeError) as erreur_gest_genr_crud:
        code, msg = erreur_gest_genr_crud.args
        flash(f"attention : {error_codes.get(code, msg)} {erreur_gest_genr_crud} ", "danger")
        flash(f"Erreur dans genre_update_wtf : {sys.exc_info()[0]} "
              f"{erreur_gest_genr_crud.args[0]} , "
              f"{erreur_gest_genr_crud}", "danger")
        flash(f"__KeyError dans genre_update_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")

    return render_template("cles/cle_update_wtf.html", form_update=form_update)


"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /genre_delete

    Test : ex. cliquer sur le menu "genres" puis cliquer sur le bouton "DELETE" d'un "genre"

    Paramètres : sans

    But : Effacer(delete) un genre qui a été sélectionné dans le formulaire "genres_afficher.html"

    Remarque :  Dans le champ "nom_genre_delete_wtf" du formulaire "genres/genre_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@obj_mon_application.route("/cle_delete", methods=['GET', 'POST'])
def cle_delete_wtf():
    data_films_attribue_genre_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_genre"
    id_cle_delete = request.values['id_genre_btn_delete_html']

    # Objet formulaire pour effacer le genre sélectionné.
    form_delete = FormWTFDeleteGenre()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("cle_fournisseur_afficher", order_by="ASC", id_cle_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "genres/genre_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_films_attribue_genre_delete = session['data_films_attribue_genre_delete']
                print("data_films_attribue_genre_delete ", data_films_attribue_genre_delete)

                flash(f"Effacer le fournisseur de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer genre" qui va irrémédiablement EFFACER le genre
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_cle": id_cle_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_cle_fournisseur = """DELETE FROM t_avoir_fournisseur WHERE fk_cle = %(value_id_cle)s"""
                str_sql_delete_cle_ouverture = """DELETE FROM t_avoir_ouverture_obj WHERE fk_cle = %(value_id_cle)s"""
                str_sql_delete_cle_lieu = """DELETE FROM t_avoir_lieu_stock WHERE fk_cle = %(value_id_cle)s"""
                str_sql_delete_cle_type = """DELETE FROM t_avoir_type WHERE fk_cle = %(value_id_cle)s"""
                str_sql_delete_id_cle = """DELETE FROM t_cle WHERE id_cle = %(value_id_cle)s"""

                # Manière brutale d'effacer d'abord la "fk_genre", même si elle n'existe pas dans la "t_genre_film"
                # Ensuite on peut effacer le genre vu qu'il n'est plus "lié" (INNODB) dans la "t_genre_film"
                with MaBaseDeDonnee() as mconn_bd:
                    mconn_bd.mabd_execute(str_sql_delete_cle_fournisseur, valeur_delete_dictionnaire)
                    mconn_bd.mabd_execute(str_sql_delete_cle_ouverture, valeur_delete_dictionnaire)
                    mconn_bd.mabd_execute(str_sql_delete_cle_lieu, valeur_delete_dictionnaire)
                    mconn_bd.mabd_execute(str_sql_delete_cle_type, valeur_delete_dictionnaire)
                    mconn_bd.mabd_execute(str_sql_delete_id_cle, valeur_delete_dictionnaire)

                flash(f"Clé définitivement effacé !!", "success")
                print(f"Clé définitivement effacé !!")

                # afficher les données
                return redirect(url_for('cle_fournisseur_afficher', order_by="ASC", id_cle_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_cle": id_cle_delete}
            print(id_cle_delete, type(id_cle_delete))

            # Requête qui affiche tous les films qui ont le genre que l'utilisateur veut effacer
            # Requête à mettre suite au lien qui est pour "type_avoir_type"
            # AND SELECT id_avoir_type, nom_type, id_cle, nom_cle, couleur FROM t_avoir_type
            str_sql_genres_films_delete = """SELECT id_avoir_fournisseur, nom_fournisseur, id_cle, nom_cle, couleur FROM t_avoir_fournisseur
                                            INNER JOIN t_fournisseur ON t_avoir_fournisseur.fk_fournisseur = t_fournisseur.id_fournisseur
                                            INNER JOIN t_cle ON t_avoir_fournisseur.fk_cle = t_cle.id_cle
                                            WHERE fk_cle = %(value_id_cle)s"""

            mybd_curseur = MaBaseDeDonnee().connexion_bd.cursor()

            mybd_curseur.execute(str_sql_genres_films_delete, valeur_select_dictionnaire)
            data_films_attribue_genre_delete = mybd_curseur.fetchall()
            print("data_films_attribue_genre_delete...", data_films_attribue_genre_delete)

            # Nécessaire pour mémoriser les données afin d'afficher à nouveau
            # le formulaire "genres/genre_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
            session['data_films_attribue_genre_delete'] = data_films_attribue_genre_delete

            # Opération sur la BD pour récupérer "id_genre" et "intitule_genre" de la "t_genre"
            str_sql_id_genre = "SELECT id_cle, nom_cle, couleur FROM t_cle WHERE id_cle = %(value_id_cle)s"

            mybd_curseur.execute(str_sql_id_genre, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()",
            # vu qu'il n'y a qu'un seul champ "nom genre" pour l'action DELETE
            data_nom_fournisseur = mybd_curseur.fetchone()
            print("data_nom_fournisseur ", data_nom_fournisseur, " type ", type(data_nom_fournisseur), " cle ",
                  data_nom_fournisseur["nom_cle"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "genre_delete_wtf.html"
            form_delete.nom_genre_delete_wtf.data = data_nom_fournisseur["nom_cle"]

            # form_delete.nom_genre_delete_wtf.data = data_nom_fournisseur["couleur"]

            # Le bouton pour l'action "DELETE" dans le form. "genre_delete_wtf.html" est caché.
            btn_submit_del = False

    # OM 2020.04.16 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
    except KeyError:
        flash(f"__KeyError dans genre_delete_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")
    except ValueError:
        flash(f"Erreur dans genre_delete_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]}", "danger")
    except (pymysql.err.OperationalError,
            pymysql.ProgrammingError,
            pymysql.InternalError,
            pymysql.err.IntegrityError,
            TypeError) as erreur_gest_genr_crud:
        code, msg = erreur_gest_genr_crud.args
        flash(f"attention : {error_codes.get(code, msg)} {erreur_gest_genr_crud} ", "danger")

        flash(f"Erreur dans genre_delete_wtf : {sys.exc_info()[0]} "
              f"{erreur_gest_genr_crud.args[0]} , "
              f"{erreur_gest_genr_crud}", "danger")

        flash(f"__KeyError dans genre_delete_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")

    return render_template("cles/cle_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_films_associes=data_films_attribue_genre_delete)
