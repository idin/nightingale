"""
Defines probability distributions for generating values.
"""

from enum import Enum
from dataclasses import dataclass
from typing import Dict, Optional, Union, List, Tuple, Set
# import sorted_dict
import numpy as np
import pandas as pd
from scipy.stats import truncnorm
from .Combination import Combination
from .helpers.density_plot import density_plot
from .helpers.sampling import generate_limited_true_samples_variable_x  # Import the function
from .helpers.SortedDict import SortedDict
from .helpers.table import StringBox, RowOfBoxes, ColumnOfBoxes

# import DistributionSet without circular import
# from .DistributionSet import DistributionSet is circular
def import_distribution_set():
    from .DistributionSet import DistributionSet
    return DistributionSet

class DistributionType(Enum):
    """Types of probability distributions"""
    NORMAL = "normal"
    UNIFORM = "uniform"
    CATEGORICAL = "categorical"
    MULTI_SELECT = "multi_select"  # New type for multiple selections

    def __str__(self):
        return f'{self.value.capitalize().replace("_", "-")}'

@dataclass(frozen=True)  # Keep it frozen if you want immutability
class Distribution:
    """A probability distribution for generating values"""
    type: Union[DistributionType, str]
    categories: Optional[Dict[str, Union[float, bool]]] = None 
    selection_probs: Optional[Dict[int, float]] = None
    min: Optional[float] = None
    max: Optional[float] = None
    mean: Optional[float] = None
    std: Optional[float] = None
    name: str = "value"  # Default column name
    alias: Optional[str] = None
    weight: Optional[float] = 1

    @classmethod
    def normal(
        cls, mean: float, std: float, name: str = "value",
        min: Optional[float] = None, max: Optional[float] = None,
    ) -> "Distribution":
        return cls(type=DistributionType.NORMAL, mean=mean, std=std, name=name, min=min, max=max)

    @classmethod
    def uniform(
        cls,
        min: float, max: float, name: str = "value",
    ) -> "Distribution":
        return cls(type=DistributionType.UNIFORM, min=min, max=max, name=name)
    
    @classmethod
    def categorical(
        cls,
        categories: Dict[str, Union[float, bool]], name: str = "value",
    ) -> "Distribution":
        return cls(type=DistributionType.CATEGORICAL, categories=categories, name=name)
    
    @classmethod
    def multi_select(
        cls,
        categories: Dict[str, Union[float, bool]], selection_probs: Dict[int, float], name: str = "value",
    ) -> "Distribution":
        return cls(type=DistributionType.MULTI_SELECT, categories=categories, selection_probs=selection_probs, name=name)
    
    def __post_init__(self):
        """Validate distribution parameters"""
        if isinstance(self.type, str):
            the_type = self.type.lower().replace('-', '').replace('_', '')
            the_type = 'multi_select' if the_type == 'multiselect' else the_type
            object.__setattr__(self, 'type', DistributionType(the_type))
        self.validate()  # Call validation method

    def __hash__(self):
        # Create a hash based on all attributes
        return hash((
            self.type,
            frozenset(self.categories.items()) if self.categories else None,
            self.selection_probs,
            self.min,
            self.max,
            self.mean,
            self.std,
            self.name
        ))

    def __eq__(self, other):
        if not isinstance(other, Distribution):
            return NotImplemented
        return (
            self.type == other.type and
            self.categories == other.categories and
            self.selection_probs == other.selection_probs and
            self.min == other.min and
            self.max == other.max and
            self.mean == other.mean and
            self.std == other.std and
            self.name == other.name
        )
    
    def is_same_distribution(self, other):
        return (
            self.type == other.type and
            self.categories == other.categories and
            self.selection_probs == other.selection_probs and
            self.min == other.min and
            self.max == other.max and
            self.mean == other.mean and
            self.std == other.std 
        )

    def validate(self):
        """Validate the distribution parameters"""
        assert self.weight != 9

        if self.type == DistributionType.NORMAL:
            if self.mean is None or self.std is None:
                raise ValueError("Normal distribution requires mean and std")
            
        elif self.type == DistributionType.UNIFORM:
            if self.min is None or self.max is None:
                raise ValueError("Uniform distribution requires min and max")
            
        elif self.type == DistributionType.CATEGORICAL:
            if not self.categories:
                raise ValueError("Categorical distribution requires categories")
            if not isinstance(self.categories, dict):
                raise TypeError("categories must be a dictionary")
            
            if not np.isclose(sum(self.categories.values()), 1.0):
                raise ValueError("Categorical probabilities must sum to 1.0")
            
        elif self.type == DistributionType.MULTI_SELECT:
            if not self.categories:
                raise ValueError("Multi-select requires categories")
            
            if any(not 0 <= p <= 1 for p in self.categories.values()):
                raise ValueError("Category probabilities must be between 0 and 1")
            
            if self.selection_probs:  # Only validate if provided
                if not np.isclose(sum(self.selection_probs.values()), 1.0):
                    raise ValueError("Selection probabilities must sum to 1.0")
                
                if max(self.selection_probs.keys()) > len(self.categories):
                    raise ValueError("Cannot select more items than available categories")
        elif not isinstance(self.type, DistributionType):
            raise TypeError("distribution type must be a DistributionType")
        else:
            raise ValueError("Unsupported distribution type")
        
            
        if self.min is not None and self.max is not None:
            if self.min > self.max:
                raise ValueError("Min must be less than max")
        if self.min is not None and self.mean is not None:
            if self.min > self.mean:
                raise ValueError("Min must be less than mean")
        if self.max is not None and self.mean is not None:
            if self.max < self.mean:
                raise ValueError("Max must be greater than mean")
            
    def copy_or_self(
            self,
            name: Optional[str] = None,
            alias: Optional[str] = None,
            min: Optional[float] = None,
            max: Optional[float] = None,
            mean: Optional[float] = None,
            std: Optional[float] = None,
            weight: Optional[float] = None
    ) -> "Distribution":
        if name is None and alias is None and min is None and max is None and mean is None and std is None and weight is None:
            return self
        else:
            return self.copy(name=name, alias=alias, min=min, max=max, mean=mean, std=std, weight=weight)

    def copy(
            self, name: Optional[str] = None, 
            alias: Optional[str] = None,
            min: Optional[float] = None, 
            max: Optional[float] = None, 
            mean: Optional[float] = None, 
            std: Optional[float] = None,
            weight: Optional[float] = None
            ) -> "Distribution":
        """Copy the distribution"""
        # Distribution is immutable, so we need to create a new one
        the_copy = Distribution(
            type=self.type,
            categories=self.categories,
            selection_probs=self.selection_probs,
            min=min or self.min,
            max=max or self.max,
            mean=mean or self.mean,
            std=std or self.std,
            name=name or self.name,
            alias=alias or self.alias,
            weight=weight or self.weight
        )
        return the_copy
    
    def _as_box(self):
        lines = [f'{self.name}: {str(self.type).capitalize().replace("_", "-")}']
        if self.type == DistributionType.UNIFORM:
            lines.append(f'min: {self.min}, max: {self.max}')
        elif self.type == DistributionType.NORMAL:
            lines.append(f'mean: {self.mean}, std: {self.std}')
            if self.min is not None and self.max is not None:
                lines.append(f'min: {self.min}, max: {self.max}')
            elif self.min is not None:
                lines.append(f'min: {self.min}')
            elif self.max is not None:
                lines.append(f'max: {self.max}')
        elif self.type == DistributionType.CATEGORICAL:
            lines.append(f'{self.categories}')
        elif self.type == DistributionType.MULTI_SELECT:
            lines.append(f'{self.categories}')
            lines.append(f'{self.selection_probs}')
        return StringBox(lines)
    
    def display_as_box(self):
        return print(self._as_box())
    
    def sample(self, n: int = 1, seed: Optional[int] = None, output_type: Optional[str] = None) -> Union[dict, pd.DataFrame]:
        """Generate samples from the distribution
        
        Args:
            n: Number of samples to generate (default: 1)
            seed: Random seed for reproducibility
            output_type: "dict" or "dataframe" (default: "dataframe")
        Returns:
            dict or pandas DataFrame of samples
        """
        if seed is not None:
            if not isinstance(seed, int):
                raise TypeError(f"seed must be an integer, got {type(seed)}")
            np.random.seed(seed)
        
        if self.type == DistributionType.UNIFORM:
            return self._sample_uniform(n, output_type)
        
        elif self.type == DistributionType.NORMAL:
            return self._sample_normal(n, output_type)
        
        elif self.type == DistributionType.CATEGORICAL:
            return self._sample_categorical(n, output_type)
        
        elif self.type == DistributionType.MULTI_SELECT:
            return self._sample_multi_select(n, output_type)
        
        else:
            raise ValueError(f"Unknown distribution type: {self.type}")
        
    @staticmethod
    def _density_plot(
            df: pd.DataFrame, x: str, 
            color: Optional[Union[str, list]] = None, title: Optional[str] = None, x_label: Optional[str] = None, y_label: Optional[str] = 'density', 
            n: int = 100, x_range: Optional[Union[list, tuple]] = None,
            separator: Optional[str] = '  ',
            bw_method: Optional[float] = 0.1
            ):
        """Create a density plot (similar to histogram) not a heatmap"""
        # do not use density_heatmap
        # first create a density curve
        # then plot it
        return density_plot(df=df, x=x, color=color, title=title, x_label=x_label, y_label=y_label, n=n, x_range=x_range, separator=separator)
        
    def plot(
            self, sample_n: int = 10000, density_n: int = 100, 
            x_range: Optional[Union[list, tuple]] = None, title: Optional[str] = None, 
            x_label: Optional[str] = None, y_label: Optional[str] = 'density', separator: Optional[str] = '  '
            ):
        """
        Plot the density of the distribution
        
        Args:
            sample_n: Number of samples to generate (default: 10000)
            density_n: Number of points to use for the density plot (default: 100)
            x_range: Range of x values to plot (default: None)
            title: Title of the plot (default: None)
            x_label: Label of the x axis (default: None)
            y_label: Label of the y axis (default: None)
            separator: Separator between x values (default: '  ')
        """
        return self._density_plot(
            df=self.sample(sample_n, output_type="dataframe"),
            x=self.name,
            color=None,
            title=title,
            x_label=x_label,
            y_label=y_label,
            n=density_n,
            x_range=x_range,
            separator=separator
        )
    
    @property
    def columns(self):
        # if the distribution is a multi_select, return the categories
        if self.type == DistributionType.MULTI_SELECT:
            return sorted(list(self.categories.keys()))
        else:
            return [self.name]

    def _sample_uniform(self, n: int, output_type: str) -> Union[dict, pd.DataFrame]:
        samples = np.random.uniform(self.min, self.max, size=n)
        
        if n == 1 and output_type != "dataframe":
            return {self.name: samples[0]}  # Use the specified column name
        
        return pd.DataFrame(samples, columns=[self.name])  # Use the specified column name
    
    @property
    def alias_or_name(self):
        return self.alias or self.name

    def _sample_normal(self, n: int, output_type: str) -> Union[dict, pd.DataFrame]:
        if self.max is None and self.min is None:
            samples = np.random.normal(self.mean, self.std, size=n)
        else:
            min = self.min or -np.inf
            max = self.max or np.inf
            a = (min - self.mean) / self.std
            b = (max - self.mean) / self.std
            samples = truncnorm.rvs(a, b, loc=self.mean, scale=self.std, size=n)
        
        if n == 1 and output_type != "dataframe":
            return {self.name: samples[0]}  # Use the specified column name
        
        return pd.DataFrame(samples, columns=[self.name])  # Use the specified column name

    def _sample_categorical(self, n: int, output_type: str) -> Union[dict, pd.DataFrame]:
        categories = list(self.categories.keys())
        probabilities = list(self.categories.values())
        samples = np.random.choice(categories, size=n, p=probabilities)
        
        if n == 1 and output_type != "dataframe":
            return {self.name: samples[0]}  # Use the specified column name
        
        return pd.DataFrame(samples, columns=[self.name])  # Use "category" as the column name

    def _sample_multi_select(self, n: int, output_type: str) -> Union[dict, pd.DataFrame]:
        samples = generate_limited_true_samples_variable_x(
            category_probs=self.categories,
            n=n,
            x_probs=self.selection_probs or {len(self.categories): 1.0},
            seed=None,
            output_type='array'
        )
        
        if n == 1 and output_type != "dataframe":
            # convert the first row of samples to a dictionary
            return {key: samples[0][i] for i, key in enumerate(self.categories.keys())}
        return pd.DataFrame(samples, columns=self.categories.keys())
    
    def __add__(self, other):
        if isinstance(other, Distribution):
            if self.name != other.name:
                other = other.copy(name=self.name)
            return CombinedDistribution(distributions=[self, other], name=self.name)
        elif isinstance(other, CombinedDistribution):
            if self.name != other.name:
                other = other.copy(name=self.name)
            other_distributions = list(other.distributions.keys())
            return CombinedDistribution(distributions=[self] + other_distributions, name=self.name)
        else:
            raise TypeError("Cannot add a distribution to a non-distribution object")
        
    def __radd__(self, other):
        return self.__add__(other)
    
    def __or__(self, other):
        return self.__add__(other)
    
    def __ror__(self, other):
        return self.__radd__(other)
    
    def __and__(self, other):
        DistributionSet = import_distribution_set()
        if isinstance(other, DistributionSet):
            return DistributionSet([self] + other.as_list, name=', '.join([self.name, other.name]))
        elif isinstance(other, (Distribution, CombinedDistribution)):
            return DistributionSet([self, other], name=', '.join([self.name, other.name]))
        else:
            raise TypeError(f"Cannot combine a distribution with a non-distribution object: {type(other)}")
        
    def __rand__(self, other):
        DistributionSet = import_distribution_set()
        if isinstance(other, DistributionSet):
            return DistributionSet(other.as_list + [self], name=', '.join([other.name, self.name]))
        elif isinstance(other, (Distribution, CombinedDistribution)):
            return DistributionSet([other, self], name=', '.join([other.name, self.name]))
        else:
            raise TypeError(f"Cannot combine a distribution with a non-distribution object: {type(other)}")

    def __mul__(self, other):
        if isinstance(other, (int, float)):
            return self.copy(weight=self.weight * other)
        else:
            raise TypeError("Cannot multiply a distribution by a non-float object")
        
    def __rmul__(self, other):
        return self.__mul__(other)
    
    def __truediv__(self, other):
        if isinstance(other, (int, float)):
            return self.copy(weight=self.weight / other)
        else:
            raise TypeError("Cannot divide a distribution by a non-float object")
        
    def tree(self):
        return self
    
class CombinedDistribution(Combination):
    """A distribution that is a combination of multiple distributions"""
    """it should be kept as a sorted dictionary"""
    objects: Dict[any, float]
    sampling_method: Optional[str] = "random"
    object_name: Optional[str] = "distribution"
    object_class: type

    @property
    def distributions(self):
        return self.objects

    def __init__(
            self, distributions: Union[Dict[Distribution, float], List[Distribution], Tuple[Distribution], Set[Distribution]], 
            sampling_method: Optional[str] = "random", name: Optional[str] = None, weight: Optional[float] = 1.0
        ):
        super().__init__(
            object_class=Distribution,
            object_name="distribution",
            objects=distributions,
            name=name,
            weight=weight,
            sampling_method=sampling_method
        )

    @property
    def name(self):
        return self._first.name
    
    @classmethod
    def _general_object(
        cls,
        object_class: any,
        objects: Union[Dict[any, float], List[any], Tuple[any], Set[any]],
        name: Optional[str] = None,
        weight: Optional[float] = 1.0,
        sampling_method: Optional[str] = "random"
    ):
        return cls(
            distributions=objects,
            name=name,
            weight=weight,
            sampling_method=sampling_method
        )
    
    def validate(self):
        super().validate()
        """Validate the combined distribution"""
        # distributions should be the same type
        # distributions can be UNIFORM and NORMAL (they are same type)
        # if distributions have categories, they should be the same
        if self._first.type in {DistributionType.UNIFORM, DistributionType.NORMAL}:
            if not all(d.type in {DistributionType.UNIFORM, DistributionType.NORMAL} for d in self.distributions.keys()):
                raise TypeError("All distributions must be UNIFORM or NORMAL")

        else:
            if not all(d.type == self._first.type for d in self.distributions.keys()):
                raise TypeError("All distributions must be the same type")

        if self._first.type == DistributionType.MULTI_SELECT:
            if not all(set(d.categories.keys()) == set(self._first.categories.keys()) for d in self.distributions.keys()):
                raise TypeError("All distributions must have the same categories")
    
    @classmethod
    def random(cls, distributions: Union[Dict[Distribution, float], List[Distribution], Tuple[Distribution], Set[Distribution]]) -> "CombinedDistribution":
        return cls(distributions=distributions, sampling_method="random")

    @classmethod
    def deterministic(cls, distributions: Union[Dict[Distribution, float], List[Distribution], Tuple[Distribution], Set[Distribution]]) -> "CombinedDistribution":
        return cls(distributions=distributions, sampling_method="deterministic")

    def plot(
            self,
            separated: bool = False,
            sample_n: int = 10000, 
            density_n: int = 100, 
            x_range: Optional[Union[list, tuple]] = None, 
            title: Optional[str] = None, 
            x_label: Optional[str] = None, 
            y_label: Optional[str] = 'density', 
            separator: Optional[str] = '  ',
            bw_method: Optional[float] = 0.1
        ) -> None:
            """
            Plot the density of the combined distribution
            """
            sample = self.sample(n=sample_n, output_type="dataframe")
            return Distribution._density_plot(
                df=sample,
                x=self.name,
                color=self.group_column if separated else None,
                title=title,
                x_label=x_label,
                y_label=y_label,
                n=density_n,
                x_range=x_range,
                separator=separator,
                bw_method=bw_method
            )

    