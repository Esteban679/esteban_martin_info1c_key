"""
    Fichier : gestion_fournisseur_crud.py
    Auteur : OM 2021.03.16
    Gestions des "routes" FLASK et des données pour les genres.
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
from APP_CLE.ouverture.gestion_ouverture_wtf_forms import *
from APP_CLE.ouverture.gestion_ouverture_wtf_forms import FormWTFAjouterOuverture
from APP_CLE.ouverture.gestion_ouverture_wtf_forms import FormWTFDeleteOuverture
from APP_CLE.ouverture.gestion_ouverture_wtf_forms import FormWTFUpdateOuverture

"""
    Auteur : OM 2021.03.16
    Définition d'une "route" /ouverture_afficher
    
    Test : ex : http://127.0.0.1:5005/ouverture_afficher
    
    Paramètres : order_by : ASC : Ascendant, DESC : Descendant
                id_genre_sel = 0 >> tous les genres.
                id_genre_sel = "n" affiche le genre dont l'id est "n"
"""


@obj_mon_application.route("/ouverture_afficher/<string:order_by>/<int:id_ouv_lieu_sel>", methods=['GET', 'POST'])
def ouverture_afficher(order_by, id_ouv_lieu_sel):
    if request.method == "GET":
        try:
            try:
                # Renvoie une erreur si la connexion est perdue.
                MaBaseDeDonnee().connexion_bd.ping(False)
            except Exception as erreur:
                flash(f"Dans Gestion genres ...terrible erreur, il faut connecter une base de donnée", "danger")
                print(f"Exception grave Classe constructeur GestionGenres {erreur.args[0]}")
                raise MaBdErreurConnexion(f"{msg_erreurs['ErreurConnexionBD']['message']} {erreur.args[0]}")

            with MaBaseDeDonnee().connexion_bd.cursor() as mc_afficher:
                if order_by == "ASC" and id_ouv_lieu_sel == 0:
                    strsql_genres_afficher = """SELECT id_ouv_lieu, nom_site_ouv, ville_ouv, rue_ouv, code_postale_ouv FROM t_ouverture_lieu ORDER BY id_ouv_lieu ASC"""
                    mc_afficher.execute(strsql_genres_afficher)
                elif order_by == "ASC":
                    # C'EST LA QUE VOUS ALLEZ DEVOIR PLACER VOTRE PROPRE LOGIQUE MySql
                    # la commande MySql classique est "SELECT * FROM t_genre"
                    # Pour "lever"(raise) une erreur s'il y a des erreurs sur les noms d'attributs dans la table
                    # donc, je précise les champs à afficher
                    # Constitution d'un dictionnaire pour associer l'id du genre sélectionné avec un nom de variable
                    valeur_id_fournisseur_selected_dictionnaire = {"value_id_ouv_lieu_selected": id_ouv_lieu_sel}
                    strsql_genres_afficher = """SELECT id_ouv_lieu, nom_site_ouv, ville_ouv, rue_ouv, code_postale_ouv FROM t_ouverture_lieu WHERE id_ouv_lieu = %(value_id_ouv_lieu_selected)s"""

                    mc_afficher.execute(strsql_genres_afficher, valeur_id_fournisseur_selected_dictionnaire)
                else:
                    strsql_genres_afficher = """SELECT id_ouv_lieu, nom_site_ouv, ville_ouv, rue_ouv, code_postale_ouv FROM t_ouverture_lieu ORDER BY id_ouv_lieu DESC"""

                    mc_afficher.execute(strsql_genres_afficher)

                data_ouverture_lieu = mc_afficher.fetchall()

                print("data_ouverture_lieu ", data_ouverture_lieu, " Type : ", type(data_ouverture_lieu))

                # Différencier les messages si la table est vide.
                if not data_ouverture_lieu and id_ouv_lieu_sel == 0:
                    flash("""La table "t_lieu_stock_cle" est vide. !!""", "warning")
                elif not data_ouverture_lieu and id_ouv_lieu_sel > 0:
                    # Si l'utilisateur change l'id_genre dans l'URL et que le genre n'existe pas,
                    flash(f"Le genre demandé n'existe pas !!", "warning")
                else:
                    # Dans tous les autres cas, c'est que la table "t_genre" est vide.
                    # OM 2020.04.09 La ligne ci-dessous permet de donner un sentiment rassurant aux utilisateurs.
                    flash(f"Données Lieu d'ouverture affichés !!", "success")

        except Exception as erreur:
            print(f"RGG Erreur générale. stock_afficher")
            # OM 2020.04.09 On dérive "Exception" par le "@obj_mon_application.errorhandler(404)"
            # fichier "run_mon_app.py"
            # Ainsi on peut avoir un message d'erreur personnalisé.
            flash(f"RGG Exception {erreur} ouverture_afficher", "danger")
            raise Exception(f"RGG Erreur générale. {erreur}")
            # raise MaBdErreurOperation(f"RGG Exception {msg_erreurs['ErreurNomBD']['message']} {erreur}")

    # Envoie la page "HTML" au serveur.
    return render_template("ouverture/ouverture_afficher.html", data=data_ouverture_lieu)


"""
    Auteur : OM 2021.03.22
    Définition d'une "route" /ouverture_ajouter
    
    Test : ex : http://127.0.0.1:5005/ouverture_ajouter
    
    Paramètres : sans
    
    But : Ajouter un genre pour un film
    
    Remarque :  Dans le champ "name_genre_html" du formulaire "ouverture/ouverture_ajouter.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@obj_mon_application.route("/ouverture_ajouter", methods=['GET', 'POST'])
def ouverture_ajouter_wtf():
    form = FormWTFAjouterOuverture()
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
                nom_site_ouv_wtf = form.nom_site_ouv_wtf.data
                nom_site_ouv = nom_site_ouv_wtf.capitalize()

                ville_ouv_wtf = form.ville_ouv_wtf.data
                ville_ouv = ville_ouv_wtf.capitalize()

                rue_ouv_wtf = form.rue_ouv_wtf.data
                rue_ouv = rue_ouv_wtf.capitalize()

                code_postale_ouv_wtf = form.code_postale_ouv_wtf.data
                code_postale_ouv = code_postale_ouv_wtf.lower()

                valeurs_insertion_dictionnaire = {"value_nom_site_ouv": nom_site_ouv,"value_ville_ouv": ville_ouv,"value_rue_ouv": rue_ouv,"value_code_postale_ouv": code_postale_ouv}
                print("valeurs_insertion_dictionnaire ", valeurs_insertion_dictionnaire)

                strsql_insert_nom_site_ouv = """INSERT INTO t_ouverture_lieu (id_ouv_lieu, nom_site_ouv, ville_ouv, rue_ouv, code_postale_ouv) VALUES (NULL,%(value_nom_site_ouv)s,%(value_ville_ouv)s,%(value_rue_ouv)s,%(value_code_postale_ouv)s)"""
                with MaBaseDeDonnee() as mconn_bd:
                    mconn_bd.mabd_execute(strsql_insert_nom_site_ouv, valeurs_insertion_dictionnaire)

                flash(f"Données insérées !!", "success")
                print(f"Données insérées !!")

                # Pour afficher et constater l'insertion de la valeur, on affiche en ordre inverse. (DESC)
                return redirect(url_for('ouverture_afficher', order_by='DESC', id_ouv_lieu_sel=0))

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

    return render_template("ouverture/ouverture_ajouter_wtf.html", form=form)


"""
    Auteur : OM 2021.03.29
    Définition d'une "route" /stock_update
    
    Test : ex cliquer sur le menu "genres" puis cliquer sur le bouton "EDIT" d'un "genre"
    
    Paramètres : sans
    
    But : Editer(update) un genre qui a été sélectionné dans le formulaire "stock_afficher.html"
    
    Remarque :  Dans le champ "nom_site_ouv_update_wtf" du formulaire "stock/stock_update_wtf.html",
                le contrôle de la saisie s'effectue ici en Python.
                On transforme la saisie en minuscules.
                On ne doit pas accepter des valeurs vides, des valeurs avec des chiffres,
                des valeurs avec des caractères qui ne sont pas des lettres.
                Pour comprendre [A-Za-zÀ-ÖØ-öø-ÿ] il faut se reporter à la table ASCII https://www.ascii-code.com/
                Accepte le trait d'union ou l'apostrophe, et l'espace entre deux mots, mais pas plus d'une occurence.
"""


@obj_mon_application.route("/ouverture_update", methods=['GET', 'POST'])
def ouverture_update_wtf():

    # L'utilisateur vient de cliquer sur le bouton "EDIT". Récupère la valeur de "id_genre"
    id_ouv_lieu_update = request.values['id_ouverture_btn_edit_html']

    # Objet formulaire pour l'UPDATE
    form_update = FormWTFUpdateOuverture()
    try:
        print(" on submit ", form_update.validate_on_submit())
        if form_update.validate_on_submit():
            # Récupèrer la valeur du champ depuis "genre_update_wtf.html" après avoir cliqué sur "SUBMIT".
            # Puis la convertir en lettres minuscules.
            nom_site_ouv_update = form_update.nom_site_ouv_update_wtf.data
            nom_site_ouv_update = nom_site_ouv_update.capitalize()

            value_ville_ouv = form_update.ville_ouv_update_wtf.data
            value_ville_ouv = value_ville_ouv.capitalize()

            value_rue_ouv = form_update.rue_ouv_update_wtf.data
            value_rue_ouv = value_rue_ouv.capitalize()

            value_code_postale_ouv = form_update.code_postale_ouv_update_wtf.data
            value_code_postale_ouv = value_code_postale_ouv.lower()

            valeur_update_dictionnaire = {"value_id_ouv_lieu": id_ouv_lieu_update, "value_nom_site_ouv": nom_site_ouv_update,
                                          "value_ville_ouv": value_ville_ouv, "value_rue_ouv": value_rue_ouv, "value_code_postale_ouv": value_code_postale_ouv}
            print("valeur_update_dictionnaire ", valeur_update_dictionnaire)

            str_sql_update_intitulegenre = """UPDATE t_ouverture_lieu SET nom_site_ouv = %(value_nom_site_ouv)s, ville_ouv = %(value_ville_ouv)s, rue_ouv = %(value_rue_ouv)s, code_postale_ouv = %(value_code_postale_ouv)s WHERE id_ouv_lieu = %(value_id_ouv_lieu)s"""
            with MaBaseDeDonnee() as mconn_bd:
                mconn_bd.mabd_execute(str_sql_update_intitulegenre, valeur_update_dictionnaire)

            flash(f"Donnée mise à jour !!", "success")
            print(f"Donnée mise à jour !!")

            # afficher et constater que la donnée est mise à jour.
            # Affiche seulement la valeur modifiée, "ASC" et l'"id_genre_update"
            return redirect(url_for('ouverture_afficher', order_by="ASC", id_ouv_lieu_sel=id_ouv_lieu_update))
        elif request.method == "GET":
            # Opération sur la BD pour récupérer "id_genre" et "intitule_genre" de la "t_genre"
            str_sql_id_genre = "SELECT id_ouv_lieu, nom_site_ouv, ville_ouv, rue_ouv, code_postale_ouv FROM t_ouverture_lieu WHERE id_ouv_lieu = %(value_id_ouv_lieu)s"
            valeur_select_dictionnaire = {"value_id_ouv_lieu": id_ouv_lieu_update}
            mybd_curseur = MaBaseDeDonnee().connexion_bd.cursor()
            mybd_curseur.execute(str_sql_id_genre, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()", vu qu'il n'y a qu'un seul champ "nom genre" pour l'UPDATE
            data_nom_site_ouv = mybd_curseur.fetchone()
            print("data_nom_site_ouv ", data_nom_site_ouv, " type ", type(data_nom_site_ouv), " genre ",
                  data_nom_site_ouv["nom_site_ouv"])

            # Afficher la valeur sélectionnée dans le champ du formulaire "genre_update_wtf.html"
            form_update.nom_site_ouv_update_wtf.data = data_nom_site_ouv["nom_site_ouv"]
            form_update.ville_ouv_update_wtf.data = data_nom_site_ouv["ville_ouv"]
            form_update.rue_ouv_update_wtf.data = data_nom_site_ouv["rue_ouv"]
            form_update.code_postale_ouv_update_wtf.data = data_nom_site_ouv["code_postale_ouv"]

    # OM 2020.04.16 ATTENTION à l'ordre des excepts, il est très important de respecter l'ordre.
    except KeyError:
        flash(f"__KeyError dans stock_update_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")
    except ValueError:
        flash(f"Erreur dans stock_update_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]}", "danger")
    except (pymysql.err.OperationalError,
            pymysql.ProgrammingError,
            pymysql.InternalError,
            pymysql.err.IntegrityError,
            TypeError) as erreur_gest_genr_crud:
        code, msg = erreur_gest_genr_crud.args
        flash(f"attention : {error_codes.get(code, msg)} {erreur_gest_genr_crud} ", "danger")
        flash(f"Erreur dans stock_update_wtf : {sys.exc_info()[0]} "
              f"{erreur_gest_genr_crud.args[0]} , "
              f"{erreur_gest_genr_crud}", "danger")
        flash(f"__KeyError dans stock_update_wtf : {sys.exc_info()[0]} {sys.exc_info()[1]} {sys.exc_info()[2]}",
              "danger")

    return render_template("ouverture/ouverture_update_wtf.html", form_update=form_update)


"""
    Auteur : OM 2021.04.08
    Définition d'une "route" /ouverture_delete
    
    Test : ex. cliquer sur le menu "genres" puis cliquer sur le bouton "DELETE" d'un "genre"
    
    Paramètres : sans
    
    But : Effacer(delete) un genre qui a été sélectionné dans le formulaire "stock_afficher.html"
    
    Remarque :  Dans le champ "nom_site_delete_wtf" du formulaire "ouverture/ouverture_delete_wtf.html",
                le contrôle de la saisie est désactivée. On doit simplement cliquer sur "DELETE"
"""


@obj_mon_application.route("/ouverture_delete", methods=['GET', 'POST'])
def ouverture_delete_wtf():
    data_films_attribue_genre_delete = None
    btn_submit_del = None
    # L'utilisateur vient de cliquer sur le bouton "DELETE". Récupère la valeur de "id_genre"
    id_ouv_lieu_delete = request.values['id_stock_btn_delete_html']

    # Objet formulaire pour effacer le genre sélectionné.
    form_delete = FormWTFDeleteOuverture()
    try:
        print(" on submit ", form_delete.validate_on_submit())
        if request.method == "POST" and form_delete.validate_on_submit():

            if form_delete.submit_btn_annuler.data:
                return redirect(url_for("ouverture_afficher", order_by="ASC", id_ouv_lieu_sel=0))

            if form_delete.submit_btn_conf_del.data:
                # Récupère les données afin d'afficher à nouveau
                # le formulaire "stock/stock_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
                data_films_attribue_genre_delete = session['data_films_attribue_genre_delete']
                print("data_films_attribue_genre_delete ", data_films_attribue_genre_delete)

                flash(f"Effacer le lieu d'ouverture de façon définitive de la BD !!!", "danger")
                # L'utilisateur vient de cliquer sur le bouton de confirmation pour effacer...
                # On affiche le bouton "Effacer genre" qui va irrémédiablement EFFACER le genre
                btn_submit_del = True

            if form_delete.submit_btn_del.data:
                valeur_delete_dictionnaire = {"value_id_ouv_lieu": id_ouv_lieu_delete}
                print("valeur_delete_dictionnaire ", valeur_delete_dictionnaire)

                str_sql_delete_cle_lieu = """DELETE FROM t_avoir_ouverture_obj WHERE fk_ouverture_obj = %(value_id_ouv_lieu)s"""
                str_sql_delete_id_cle = """DELETE FROM t_ouverture_lieu WHERE id_ouv_lieu = %(value_id_ouv_lieu)s"""

                # Manière brutale d'effacer d'abord la "fk_genre", même si elle n'existe pas dans la "t_genre_film"
                # Ensuite on peut effacer le genre vu qu'il n'est plus "lié" (INNODB) dans la "t_genre_film"
                with MaBaseDeDonnee() as mconn_bd:
                    mconn_bd.mabd_execute(str_sql_delete_cle_lieu, valeur_delete_dictionnaire)
                    mconn_bd.mabd_execute(str_sql_delete_id_cle, valeur_delete_dictionnaire)

                flash(f"Lieu de stock définitivement effacé !!", "success")
                print(f"Lieu de stock définitivement effacé !!")

                # afficher les données
                return redirect(url_for('ouverture_afficher', order_by="ASC", id_ouv_lieu_sel=0))

        if request.method == "GET":
            valeur_select_dictionnaire = {"value_id_ouv_lieu": id_ouv_lieu_delete}
            print(id_ouv_lieu_delete, type(id_ouv_lieu_delete))

            # Requête qui affiche tous les films qui ont le genre que l'utilisateur veut effacer
            # Requête à mettre suite au lien qui est pour "type_avoir_type"
            str_sql_genres_films_delete = """SELECT id_avoir_ouverture_obj, nom_cle, id_ouv_lieu, nom_site_ouv, ville_ouv, rue_ouv, code_postale_ouv FROM t_avoir_ouverture_obj
                                            INNER JOIN t_cle ON t_avoir_ouverture_obj.fk_cle = t_cle.id_cle
                                            INNER JOIN t_ouverture_lieu ON t_avoir_ouverture_obj.fk_ouverture_obj = t_ouverture_lieu.id_ouv_lieu
                                            WHERE fk_ouverture_obj = %(value_id_ouv_lieu)s"""

            mybd_curseur = MaBaseDeDonnee().connexion_bd.cursor()

            mybd_curseur.execute(str_sql_genres_films_delete, valeur_select_dictionnaire)
            data_films_attribue_genre_delete = mybd_curseur.fetchall()
            print("data_films_attribue_genre_delete...", data_films_attribue_genre_delete)

            # Nécessaire pour mémoriser les données afin d'afficher à nouveau
            # le formulaire "genres/genre_delete_wtf.html" lorsque le bouton "Etes-vous sur d'effacer ?" est cliqué.
            session['data_films_attribue_genre_delete'] = data_films_attribue_genre_delete

            # Opération sur la BD pour récupérer "id_genre" et "intitule_genre" de la "t_genre"
            str_sql_id_genre = "SELECT id_ouv_lieu, nom_site_ouv, ville_ouv, rue_ouv, code_postale_ouv FROM t_ouverture_lieu WHERE id_ouv_lieu = %(value_id_ouv_lieu)s"

            mybd_curseur.execute(str_sql_id_genre, valeur_select_dictionnaire)
            # Une seule valeur est suffisante "fetchone()",
            # vu qu'il n'y a qu'un seul champ "nom genre" pour l'action DELETE
            #data_nom_lieu_stock_cle = mybd_curseur.fetchone()
            #data_nom_ville = mybd_curseur.fetchone()
            data_nom_rue_ouv = mybd_curseur.fetchone()

            #print("data_nom_lieu_stock_cle ", data_nom_lieu_stock_cle, " type ", type(data_nom_lieu_stock_cle), " cle ",
            #      data_nom_lieu_stock_cle["nom_site"])
            #print("data_nom_ville ", data_nom_ville, " type ", type(data_nom_ville), " cle ",
            #      data_nom_ville["ville"])
            print("data_nom_rue_ouv ", data_nom_rue_ouv, " type ", type(data_nom_rue_ouv), " rue ",
                  data_nom_rue_ouv["rue_ouv"],
                  "code postale ouverture", data_nom_rue_ouv ["code_postale_ouv"],
                  "ville ouverture", data_nom_rue_ouv ["ville_ouv"],
                  "nom site ouverture", data_nom_rue_ouv ["nom_site_ouv"])



            # Afficher la valeur sélectionnée dans le champ du formulaire "genre_delete_wtf.html"
            form_delete.rue_ouv_delete_wtf.data = data_nom_rue_ouv["rue_ouv"]
            form_delete.ville_ouv_delete_wtf.data = data_nom_rue_ouv["ville_ouv"]
            form_delete.nom_site_ouv_delete_wtf.data = data_nom_rue_ouv["nom_site_ouv"]
            form_delete.code_postale_ouv_delete_wtf.data = data_nom_rue_ouv["code_postale_ouv"]

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

    return render_template("ouverture/ouverture_delete_wtf.html",
                           form_delete=form_delete,
                           btn_submit_del=btn_submit_del,
                           data_films_associes=data_films_attribue_genre_delete)
