"""
    Fichier : gestion_genres_wtf_forms.py
    Auteur : OM 2021.03.22
    Gestion des formulaires avec WTF
"""
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import Length
from wtforms.validators import Regexp


class FormWTFAjouterOuverture(FlaskForm):
    """
        Dans le formulaire "genres_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    ajouter_restricted_all_ouverture = "^[a-zA-ZÀ_.-]*$"
    nom_site_ouv_wtf = StringField("Clavioter le nom du site ", validators=[Length(min=2, max=25, message="min 2 max 25"),
                                                                   Regexp(ajouter_restricted_all_ouverture,
                                                                          message="Pas de chiffres, de caractères "
                                                                                  "spéciaux, "
                                                                                  "d'espace à double, de double "
                                                                                  "apostrophe, de double trait union")
                                                                   ])

    ville_ouv_wtf = StringField("Clavioter le nom de la ville ",
                                          validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                      Regexp(ajouter_restricted_all_ouverture,
                                                             message="Pas de chiffres, de caractères "
                                                                     "spéciaux, "
                                                                     "d'espace à double, de double "
                                                                     "apostrophe, de double trait union")
                                                      ])
    ajouter_ouverture_regexp = "^[a-zA-Z0-9_.-]*$"
    rue_ouv_wtf = StringField("Clavioter le nom de la rue",
                                    validators=[Length(min=2, max=25, message="min 2 max 25"),
                                                Regexp(ajouter_ouverture_regexp,
                                                       message="Pas de caractères "
                                                               "spéciaux, "
                                                               "d'espace à double, de double "
                                                               "apostrophe, de double trait union")
                                                ])
    ajouter_code_postale_regexp = "^[0-9]+$"
    code_postale_ouv_wtf = StringField("Clavioter le code postal",
                                    validators=[Length(min=4, max=6, message="min 4 max 6"),
                                                Regexp(ajouter_code_postale_regexp,
                                                       message="Pas de lettres, de caractères "
                                                               "spéciaux, "
                                                               "d'espace à double, de double "
                                                               "apostrophe, de double trait union")
                                                ])
    submit = SubmitField("Enregistrer le lieu d'ouverture")


class FormWTFUpdateOuverture(FlaskForm):
    """
        Dans le formulaire "genre_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    update_restricted_regexp = "^[a-zA-ZÀ_.-]*$"
    nom_site_ouv_update_wtf = StringField("Editer le nom du site ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                          Regexp(update_restricted_regexp,
                                                                                 message="Pas de chiffres, de "
                                                                                         "caractères "
                                                                                         "spéciaux, "
                                                                                         "d'espace à double, de double "
                                                                                         "apostrophe, de double trait "
                                                                                         "union")
                                                                          ])
    ville_ouv_update_wtf = StringField("Editer le nom de la ville", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                          Regexp(update_restricted_regexp,
                                                                                 message="Pas de chiffres, de "
                                                                                         "caractères "
                                                                                         "spéciaux, "
                                                                                         "d'espace à double, de double "
                                                                                         "apostrophe, de double trait "
                                                                                         "union")
                                                                          ])
    update_ouverture_regexp = "^[a-zA-Z0-9_.-]*$"
    rue_ouv_update_wtf = StringField("Editer le nom de la rue ", validators=[Length(min=2, max=25, message="min 2 max 25"),
                                                                        Regexp(update_ouverture_regexp,
                                                                               message="Pas de chiffres, de "
                                                                                       "caractères "
                                                                                       "spéciaux, "
                                                                                       "d'espace à double, de double "
                                                                                       "apostrophe, de double trait "
                                                                                       "union")
                                                                        ])
    code_postale_ouv_update_regexp = "^[0-9]+$"
    code_postale_ouv_update_wtf = StringField("Editer le code postal", validators=[Length(min=4, max=6, message="min 4 max 6"),
                                                                        Regexp(code_postale_ouv_update_regexp,
                                                                               message="Pas de chiffres, de "
                                                                                       "caractères "
                                                                                       "spéciaux, "
                                                                                       "d'espace à double, de double "
                                                                                       "apostrophe, de double trait "
                                                                                       "union")
                                                                        ])
    submit = SubmitField("Update Lieu d'ouverture")


class FormWTFDeleteOuverture(FlaskForm):
    """
        Dans le formulaire "genre_delete_wtf.html"

        nom_genre_delete_wtf : Champ qui reçoit la valeur du genre, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "genre".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_genre".
    """
    rue_ouv_delete_wtf = StringField("Effacer cette rue du lieu d'ouverture")
    ville_ouv_delete_wtf = StringField("Effacer cette ville du lieu d'ouverture")
    nom_site_ouv_delete_wtf = StringField("Effacer ce site du lieu d'ouverture")
    code_postale_ouv_delete_wtf = StringField("Effacer ce code postal du lieu d'ouverture")
    submit_btn_del = SubmitField("Effacer ce lieu de ce stock")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
