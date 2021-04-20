from canari.maltego.message import Entity

__author__ = "Censys Team"
__copyright__ = "Copyright 2021, censys Project"
__credits__ = ["Aidan Holland"]

__license__ = "GPLv3"
__version__ = "0.1"
__maintainer__ = "Censys Team"
__email__ = "support@censys.io"
__status__ = "Development"

__all__ = ["CensysEntity"]


class CensysEntity(Entity):
    """This is the base entity used to optionally define the namespace for all your other entities. The namespace is the
    string preceding the name of your entity separated by a dot (i.e. 'foo' in 'foo.BarTransform'). If _namespace_ is
    not defined as a class variable, then the namespace will be generated based on the name of your Canari package. For
    example, if your project's name is 'sniffmypackets' then the namespace will also be 'sniffmypackets'.
    """
    pass
