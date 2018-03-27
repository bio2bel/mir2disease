# -*- coding: utf-8 -*-

import logging

import pybel
from pybel import BELGraph
from tqdm import tqdm

from bio2bel.abstractmanager import AbstractManager
from .constants import MODULE_NAME
from .models import Base, Disease, MiRNA, Relationship
from .parser import get_mir2disease_df

__all__ = ['Manager']

log = logging.getLogger(__name__)


class Manager(AbstractManager):
    module_name = MODULE_NAME

    def __init__(self, connection=None):
        super(Manager, self).__init__(connection=connection)

        self.name_mirna = {}
        self.name_disease = {}

    @property
    def base(self):
        return Base

    def get_mirna_by_name(self, name):
        """Gets an miRNA from the database if it exists

        :param str name: A mirBase name
        :rtype: Optional[MiRNA]
        """
        return self.session.query(MiRNA).filter(MiRNA.name == name).one_or_none()

    def get_disease_by_name(self, name):
        """Gets a Disease from the database if it exists

        :param str name: A MeSH disease name
        :rtype: Optional[Disease]
        """
        return self.session.query(Disease).filter(Disease.name == name).one_or_none()

    def get_or_create_mirna(self, name):
        """Gets an miRNA from the database or creates it if it does not exist

        :param str name: A mirBase name
        :rtype: MiRNA
        """
        mirna = self.name_mirna.get(name)
        if mirna is not None:
            return mirna

        mirna = self.get_mirna_by_name(name)
        if mirna is not None:
            self.name_mirna[name] = mirna
            return mirna

        mirna = self.name_mirna[name] = MiRNA(name=name)
        self.session.add(mirna)

        return mirna

    def get_or_create_disease(self, name):
        """Gets a Disease from the database or creates it if it does not exist

        :param str name: A MeSH disease name
        :rtype: Disease
        """
        disease = self.name_disease.get(name)
        if disease is not None:
            return disease

        disease = self.get_disease_by_name(name)
        if disease is not None:
            self.name_disease[name] = disease
            return disease

        disease = self.name_disease[name] = Disease(name=name)
        self.session.add(disease)

        return disease

    def count_mirnas(self):
        """Counts the number of miRNAs in the database

        :rtype: int
        """
        return self._count_model(MiRNA)

    def count_diseases(self):
        """Counts the number of diseases in the database

        :rtype: int
        """
        return self._count_model(Disease)

    def count_relationships(self):
        """Counts the number of miRNA-disease relationships in the database

        :rtype: int
        """
        return self._count_model(Relationship)

    def populate(self, url=None):
        """Populates the database

        :param Optional[str] url: A custom data source URL
        """
        df = get_mir2disease_df(url=url)

        log.info('building models')
        for _, idx, mirna_name, disease_name, pubmed, description in tqdm(df.itertuples(), total=len(df.index)):
            mirna = self.get_or_create_mirna(mirna_name)
            disease = self.get_or_create_disease(disease_name)

            relationship = Relationship(
                description=description,
                mirna=mirna,
                disease=disease,
            )

            self.session.add(relationship)

        log.info('inserting models')
        self.session.commit()

    def get_relationships(self):
        """Returns all relationships

        :rtype: list[Relationship]
        """
        return self.session.query(Relationship).all()

    def to_bel_graph(self):
        """Builds a BEL graph containing all of the miRNA-disease relationships in the database

        :rtype: BELGraph
        """
        graph = BELGraph()

        for relationship in self.get_relationships():
            relationship.add_to_bel_graph(graph)

        return graph

    def to_bel_file(self, file):
        graph = self.to_bel_graph()
        pybel.to_bel(graph, file=file)

    def upload_bel(self, connection=None):
        graph = self.to_bel_graph()
        pybel.to_database(graph, connection=connection)
