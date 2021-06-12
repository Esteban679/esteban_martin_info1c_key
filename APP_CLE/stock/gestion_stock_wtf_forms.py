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


class FormWTFAjouterStock(FlaskForm):
    """
        Dans le formulaire "genres_ajouter_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    ajouter_stock_regexp = "^[a-zA-Z_.-]*$"
    nom_site_wtf = StringField("Clavioter le nom du site ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                   Regexp(ajouter_stock_regexp,
                                                                          message="Pas de chiffres, de caractères "
                                                                                  "spéciaux, "
                                                                                  "d'espace à double, de double "
                                                                                  "apostrophe, de double trait union")
                                                                   ])
    ville_wtf = StringField("Clavioter le nom de la ville ",
                                          validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                      Regexp(ajouter_stock_regexp,
                                                             message="Pas de chiffres, de caractères "
                                                                     "spéciaux, "
                                                                     "d'espace à double, de double "
                                                                     "apostrophe, de double trait union")
                                                      ])
    ajouter_stock_regxp = "^[a-zA-Z0-9_.-]*$"
    rue_wtf = StringField("Clavioter le nom de la rue",
                                    validators=[Length(min=2, max=25, message="min 2 max 25"),
                                                Regexp(ajouter_stock_regxp,
                                                       message="Pas de chiffres, de caractères "
                                                               "spéciaux, "
                                                               "d'espace à double, de double "
                                                               "apostrophe, de double trait union")
                                                ])
    ajouter_code_postale_regexp = "^[0-9]+$"
    code_postale_wtf = StringField("Clavioter le code postal",
                                    validators=[Length(min=4, max=6, message="min 4 max 6"),
                                                Regexp(ajouter_code_postale_regexp,
                                                       message="Que des chiffres")
                                                ])
    submit = SubmitField("Enregistrer la clé")


class FormWTFUpdateStock(FlaskForm):
    """
        Dans le formulaire "genre_update_wtf.html" on impose que le champ soit rempli.
        Définition d'un "bouton" submit avec un libellé personnalisé.
    """
    update_stock_regexp = "^([A-Z]|[a-zÀ-ÖØ-öø-ÿ])[A-Za-zÀ-ÖØ-öø-ÿ]*['\- ]?[A-Za-zÀ-ÖØ-öø-ÿ]+$"
    nom_site_update_wtf = StringField("Clavioter le nom du site ", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                          Regexp(update_stock_regexp,
                                                                                 message="Pas de chiffres, de "
                                                                                         "caractères "
                                                                                         "spéciaux, "
                                                                                         "d'espace à double, de double "
                                                                                         "apostrophe, de double trait "
                                                                                         "union")
                                                                          ])
    ville_update_wtf = StringField("Clavioter le nom de la ville", validators=[Length(min=2, max=20, message="min 2 max 20"),
                                                                          Regexp(update_stock_regexp,
                                                                                 message="Pas de chiffres, de "
                                                                                         "caractères "
                                                                                         "spéciaux, "
                                                                                         "d'espace à double, de double "
                                                                                         "apostrophe, de double trait "
                                                                                         "union")
                                                                          ])
    modifier_stock_regxp = "^[a-zA-Z0-9_.-]*$"
    rue_update_wtf = StringField("Clavioter le nom de la rue ", validators=[Length(min=2, max=25, message="min 2 max 25"),
                                                                        Regexp(modifier_stock_regxp,
                                                                               message="Remplacer les espace par des traits, "
                                                                                       "pas de caractères spéciaux, "
                                                                                       "pas d'apostrophe"
                                                                                       "union")
                                                                        ])
    code_postale_update_regexp = "^[a-zA-Z0-9_.-]*$"
    code_postale_update_wtf = StringField("Clavioter le code postal", validators=[Length(min=4, max=6, message="min 4 max 6"),
                                                                        Regexp(code_postale_update_regexp,
                                                                               message="Pas de chiffres, de "
                                                                                       "caractères "
                                                                                       "spéciaux, "
                                                                                       "d'espace à double, de double "
                                                                                       "apostrophe, de double trait "
                                                                                       "union")
                                                                        ])
    submit = SubmitField("Update Lieu de stock")


class FormWTFDeleteStock(FlaskForm):
    """
        Dans le formulaire "genre_delete_wtf.html"

        nom_genre_delete_wtf : Champ qui reçoit la valeur du genre, lecture seule. (readonly=true)
        submit_btn_del : Bouton d'effacement "DEFINITIF".
        submit_btn_conf_del : Bouton de confirmation pour effacer un "genre".
        submit_btn_annuler : Bouton qui permet d'afficher la table "t_genre".
    """
    rue_delete_wtf = StringField("Effacer ce lieu ce stock")
    ville_delete_wtf = StringField("Effacer ce lieu ce stock")
    nom_site_delete_wtf = StringField("Effacer ce lieu ce stock")
    code_postale_delete_wtf = StringField("Effacer ce lieu ce stock")
    submit_btn_del = SubmitField("Effacer ce lieu de ce stock")
    submit_btn_conf_del = SubmitField("Etes-vous sur d'effacer ?")
    submit_btn_annuler = SubmitField("Annuler")
