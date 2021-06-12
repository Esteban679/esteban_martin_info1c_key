-- phpMyAdmin SQL Dump
-- version 4.5.4.1
-- http://www.phpmyadmin.net
--
-- Client :  localhost
-- Généré le :  Mar 25 Mai 2021 à 12:51
-- Version du serveur :  5.7.11
-- Version de PHP :  7.0.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données :  `martin_esteban_info1c`
--

DROP DATABASE IF EXISTS martin_esteban_info1c;

-- Création d'un nouvelle base de donnée

CREATE DATABASE IF NOT EXISTS martin_esteban_info1c;

-- Utilisation de cette base de donnée

USE martin_esteban_info1c;
-- --------------------------------------------------------

--
-- Structure de la table `t_avoir_fournisseur`
--

CREATE TABLE `t_avoir_fournisseur` (
  `id_avoir_fournisseur` int(11) NOT NULL,
  `fk_cle` int(11) NOT NULL,
  `fk_fournisseur` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_avoir_fournisseur`
--

INSERT INTO `t_avoir_fournisseur` (`id_avoir_fournisseur`, `fk_cle`, `fk_fournisseur`) VALUES
(6, 4, 2);

-- --------------------------------------------------------

--
-- Structure de la table `t_avoir_lieu_stock`
--

CREATE TABLE `t_avoir_lieu_stock` (
  `id_avoir_lieu_stock` int(11) NOT NULL,
  `fk_cle` int(11) NOT NULL,
  `fk_lieu_stock_cle` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `t_avoir_ouverture_obj`
--

CREATE TABLE `t_avoir_ouverture_obj` (
  `id_avoir_ouverture_obj` int(11) NOT NULL,
  `fk_cle` int(11) NOT NULL,
  `fk_ouverture_obj` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `t_avoir_type`
--

CREATE TABLE `t_avoir_type` (
  `id_avoir_type` int(11) NOT NULL,
  `fk_cle` int(11) NOT NULL,
  `fk_type_cle` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Structure de la table `t_cle`
--

CREATE TABLE `t_cle` (
  `id_cle` int(11) NOT NULL,
  `nom_cle` varchar(43) NOT NULL,
  `couleur` varchar(43) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_cle`
--

INSERT INTO `t_cle` (`id_cle`, `nom_cle`, `couleur`) VALUES
(4, 'Clé 04', 'Bleu'),
(5, 'cleun', 'vert');

-- --------------------------------------------------------

--
-- Structure de la table `t_fournisseur`
--

CREATE TABLE `t_fournisseur` (
  `id_fournisseur` int(11) NOT NULL,
  `nom_fournisseur` varchar(42) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_fournisseur`
--

INSERT INTO `t_fournisseur` (`id_fournisseur`, `nom_fournisseur`) VALUES
(1, 'HP'),
(2, 'Logitech'),
(3, 'Apple'),
(5, 'samsung');

-- --------------------------------------------------------

--
-- Structure de la table `t_lieu_stock_cle`
--

CREATE TABLE `t_lieu_stock_cle` (
  `id_lieu_stock_cle` int(11) NOT NULL,
  `nom_site` varchar(42) NOT NULL,
  `ville` varchar(42) NOT NULL,
  `rue` varchar(42) NOT NULL,
  `code_postale` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_lieu_stock_cle`
--

INSERT INTO `t_lieu_stock_cle` (`id_lieu_stock_cle`, `nom_site`, `ville`, `rue`, `code_postale`) VALUES
(1, 'Perrelet', 'Lausanne', 'Route des Bisounours 45', 1001),
(2, 'Ouchy-Olympique', 'Bex', 'Rue de la Cygogne 76', 1234),
(3, 'OK', 'Bex', 'Rue du bois 90', 1888);

-- --------------------------------------------------------

--
-- Structure de la table `t_ouverture_lieu`
--

CREATE TABLE `t_ouverture_lieu` (
  `id_ouv_lieu` int(11) NOT NULL,
  `nom_site_ouv` varchar(42) NOT NULL,
  `ville_ouv` varchar(42) NOT NULL,
  `rue_ouv` varchar(42) NOT NULL,
  `code_postale_ouv` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_ouverture_lieu`
--

INSERT INTO `t_ouverture_lieu` (`id_ouv_lieu`, `nom_site_ouv`, `ville_ouv`, `rue_ouv`, `code_postale_ouv`) VALUES
(1, 'Perosalle', 'Ollon', 'Chemin des Cheveux 45', 1001),
(2, 'Collège d\'en haut ', 'Lausanne', 'Rue de la calvitie 32', 1234),
(3, 'Perrelet', 'Lausanne', 'Rue des oeufs 65', 1888);

-- --------------------------------------------------------

--
-- Structure de la table `t_type_cle`
--

CREATE TABLE `t_type_cle` (
  `id_type_cle` int(11) NOT NULL,
  `nom_type` varchar(42) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Contenu de la table `t_type_cle`
--

INSERT INTO `t_type_cle` (`id_type_cle`, `nom_type`) VALUES
(1, 'coffre'),
(2, 'voiture'),
(3, 'Porte');

--
-- Index pour les tables exportées
--

--
-- Index pour la table `t_avoir_fournisseur`
--
ALTER TABLE `t_avoir_fournisseur`
  ADD PRIMARY KEY (`id_avoir_fournisseur`),
  ADD KEY `fk_cle` (`fk_cle`),
  ADD KEY `fk_fournisseur` (`fk_fournisseur`);

--
-- Index pour la table `t_avoir_lieu_stock`
--
ALTER TABLE `t_avoir_lieu_stock`
  ADD PRIMARY KEY (`id_avoir_lieu_stock`),
  ADD KEY `fk_cle` (`fk_cle`),
  ADD KEY `fk_lieu_stock_cle` (`fk_lieu_stock_cle`);

--
-- Index pour la table `t_avoir_ouverture_obj`
--
ALTER TABLE `t_avoir_ouverture_obj`
  ADD PRIMARY KEY (`id_avoir_ouverture_obj`),
  ADD KEY `fk_cle` (`fk_cle`),
  ADD KEY `fk_ouverture_obj` (`fk_ouverture_obj`);

--
-- Index pour la table `t_avoir_type`
--
ALTER TABLE `t_avoir_type`
  ADD PRIMARY KEY (`id_avoir_type`),
  ADD KEY `fk_cle` (`fk_cle`),
  ADD KEY `fk_type_cle` (`fk_type_cle`);

--
-- Index pour la table `t_cle`
--
ALTER TABLE `t_cle`
  ADD PRIMARY KEY (`id_cle`);

--
-- Index pour la table `t_fournisseur`
--
ALTER TABLE `t_fournisseur`
  ADD PRIMARY KEY (`id_fournisseur`);

--
-- Index pour la table `t_lieu_stock_cle`
--
ALTER TABLE `t_lieu_stock_cle`
  ADD PRIMARY KEY (`id_lieu_stock_cle`);

--
-- Index pour la table `t_ouverture_lieu`
--
ALTER TABLE `t_ouverture_lieu`
  ADD PRIMARY KEY (`id_ouv_lieu`);

--
-- Index pour la table `t_type_cle`
--
ALTER TABLE `t_type_cle`
  ADD PRIMARY KEY (`id_type_cle`);

--
-- AUTO_INCREMENT pour les tables exportées
--

--
-- AUTO_INCREMENT pour la table `t_avoir_fournisseur`
--
ALTER TABLE `t_avoir_fournisseur`
  MODIFY `id_avoir_fournisseur` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
--
-- AUTO_INCREMENT pour la table `t_avoir_lieu_stock`
--
ALTER TABLE `t_avoir_lieu_stock`
  MODIFY `id_avoir_lieu_stock` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `t_avoir_ouverture_obj`
--
ALTER TABLE `t_avoir_ouverture_obj`
  MODIFY `id_avoir_ouverture_obj` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `t_avoir_type`
--
ALTER TABLE `t_avoir_type`
  MODIFY `id_avoir_type` int(11) NOT NULL AUTO_INCREMENT;
--
-- AUTO_INCREMENT pour la table `t_cle`
--
ALTER TABLE `t_cle`
  MODIFY `id_cle` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- AUTO_INCREMENT pour la table `t_fournisseur`
--
ALTER TABLE `t_fournisseur`
  MODIFY `id_fournisseur` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- AUTO_INCREMENT pour la table `t_lieu_stock_cle`
--
ALTER TABLE `t_lieu_stock_cle`
  MODIFY `id_lieu_stock_cle` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT pour la table `t_ouverture_lieu`
--
ALTER TABLE `t_ouverture_lieu`
  MODIFY `id_ouv_lieu` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT pour la table `t_type_cle`
--
ALTER TABLE `t_type_cle`
  MODIFY `id_type_cle` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- Contraintes pour les tables exportées
--

--
-- Contraintes pour la table `t_avoir_fournisseur`
--
ALTER TABLE `t_avoir_fournisseur`
  ADD CONSTRAINT `t_avoir_fournisseur_ibfk_1` FOREIGN KEY (`fk_cle`) REFERENCES `t_cle` (`id_cle`),
  ADD CONSTRAINT `t_avoir_fournisseur_ibfk_2` FOREIGN KEY (`fk_fournisseur`) REFERENCES `t_fournisseur` (`id_fournisseur`);

--
-- Contraintes pour la table `t_avoir_lieu_stock`
--
ALTER TABLE `t_avoir_lieu_stock`
  ADD CONSTRAINT `t_avoir_lieu_stock_ibfk_1` FOREIGN KEY (`fk_cle`) REFERENCES `t_cle` (`id_cle`),
  ADD CONSTRAINT `t_avoir_lieu_stock_ibfk_2` FOREIGN KEY (`fk_lieu_stock_cle`) REFERENCES `t_lieu_stock_cle` (`id_lieu_stock_cle`);

--
-- Contraintes pour la table `t_avoir_ouverture_obj`
--
ALTER TABLE `t_avoir_ouverture_obj`
  ADD CONSTRAINT `t_avoir_ouverture_obj_ibfk_1` FOREIGN KEY (`fk_cle`) REFERENCES `t_cle` (`id_cle`),
  ADD CONSTRAINT `t_avoir_ouverture_obj_ibfk_2` FOREIGN KEY (`fk_ouverture_obj`) REFERENCES `t_ouverture_lieu` (`id_ouv_lieu`);

--
-- Contraintes pour la table `t_avoir_type`
--
ALTER TABLE `t_avoir_type`
  ADD CONSTRAINT `t_avoir_type_ibfk_1` FOREIGN KEY (`fk_cle`) REFERENCES `t_cle` (`id_cle`),
  ADD CONSTRAINT `t_avoir_type_ibfk_2` FOREIGN KEY (`fk_type_cle`) REFERENCES `t_type_cle` (`id_type_cle`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
