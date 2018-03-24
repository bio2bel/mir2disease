# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from .constants import MODULE_NAME

from pybel.dsl import mirna as mirna_dsl, pathology as pathology_dsl
from pybel.constants import ASSOCIATION

MIRNA_TABLE_NAME = '{}_mirna'.format(MODULE_NAME)
DISEASE_TABLE_NAME = '{}_disease'.format(MODULE_NAME)
RELATIONSHIP_TABLE_NAME = '{}_relationship'.format(MODULE_NAME)

Base = declarative_base()


class MiRNA(Base):
    """This class represents the miRNA table"""

    __tablename__ = MIRNA_TABLE_NAME
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True, index=True, doc='name from mirBase')

    def __repr__(self):
        return self.name


class Disease(Base):
    """This class represents the disease table"""

    __tablename__ = DISEASE_TABLE_NAME
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True, index=True, doc='name from MeSH')

    def __repr__(self):
        return self.name


class Relationship(Base):
    """This class represents the miRNA disease relationship table"""

    __tablename__ = RELATIONSHIP_TABLE_NAME
    id = Column(Integer, primary_key=True)
    description = Column(String, doc='This is a manually curated relationship')
    mirna_id = Column(Integer, ForeignKey('{}.id'.format(MIRNA_TABLE_NAME)))
    mirna = relationship('MiRNA')
    disease_id = Column(Integer, ForeignKey('{}.id'.format(DISEASE_TABLE_NAME)))
    disease = relationship('Disease')

    def add_to_bel_graph(self, graph):
        """Add this relationship to a BEL graph

        :param pybel.BELGraph graph:
        """
        mirna_node = mirna_dsl(namespace='MIRBASE', name=self.mirna.name)
        disease_node = pathology_dsl(namespace='MESH', name=self.disease.name)
        #TODO: @Charlie. Define valid relationship type. Corpus contains more information than ASSOCIATION
        graph.add_qualified_edge(
            mirna_node,
            disease_node,
            relation=ASSOCIATION,
            evidence=str(self.description),
        )
