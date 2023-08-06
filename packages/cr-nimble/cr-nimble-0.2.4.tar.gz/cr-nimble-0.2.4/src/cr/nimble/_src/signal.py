# Copyright 2021 CR.Sparse Development Team
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import jax
import jax.numpy as jnp
from jax import random, jit
import jax.numpy.fft as jfft
from jax.scipy import signal

from cr.nimble import sqr_norms_l2_cw, sqr_norms_l2_rw
from cr.nimble import is_matrix
from .discrete.number import next_pow_of_2

def find_first_signal_with_energy_le_rw(X, energy):
    """Returns the index of the first row which has energy less than the specified threshold
    """
    assert is_matrix(X)
    energies = sqr_norms_l2_rw(X)
    index = jnp.argmax(energies <= energy)
    return index if energies[index] <= energy else jnp.array(-1)

def find_first_signal_with_energy_le_cw(X, energy):
    """Returns the index of the first column which has energy less than the specified threshold
    """
    assert is_matrix(X)
    energies = sqr_norms_l2_cw(X)
    index = jnp.argmax(energies <= energy)
    return index if energies[index] <= energy else jnp.array(-1)


def randomize_rows(key, X):
    """Randomizes the rows in X

    Args:
        key: a PRNG key used as the random key.
        X (jax.numpy.ndarray): A 2D data matrix

    Returns:
        (jax.numpy.ndarray): The data matrix with randomized rows
    """
    assert is_matrix(X)
    m, n = X.shape
    r = random.permutation(key, m)
    return X[r, :]

def randomize_cols(key, X):
    """Randomizes the columns in X

    Args:
        key: a PRNG key used as the random key.
        X (jax.numpy.ndarray): A 2D data matrix

    Returns:
        (jax.numpy.ndarray): The data matrix with randomized columns
    """
    assert is_matrix(X)
    m, n = X.shape
    r = random.permutation(key, n)
    return X[:, r]


def largest_indices(x, K):
    """Returns the indices of K largest entries in x by magnitude

    Args:
        x (jax.numpy.ndarray): An data vector/point
        K (int): The number of largest entries to be identified in x

    Returns:
        (jax.numpy.ndarray): An index vector of size K identifying the K largest entries in x
        in descending order
    """
    indices = jnp.argsort(jnp.abs(x))
    return indices[:-K-1:-1]

def largest_indices_rw(X, K):
    """Returns the indices of K largest entries by magnitude in each row of X

    Args:
        X (jax.numpy.ndarray): An (S,N) data matrix with data points in rows
        K (int): The number of largest entries to be identified in each row of X

    Returns:
        (jax.numpy.ndarray): An (S,K) index matrix indices of K largest elements in each row of X
    """
    indices = jnp.argsort(jnp.abs(X), axis=1)
    return indices[:, :-K-1:-1]

def largest_indices_cw(X, K):
    """Returns the indices of K largest entries by magnitude in each column of X

    Args:
        X (jax.numpy.ndarray): An (N,S) data matrix with data points in columns
        K (int): The number of largest entries to be identified in each column of X

    Returns:
        (jax.numpy.ndarray): An (K,S) index matrix indices of K largest elements in each column of X
    """
    indices = jnp.argsort(jnp.abs(X), axis=0)
    return indices[:-K-1:-1, :]

def take_along_rows(X, indices):
    """Picks K entries from each row of X specified by indices matrix

    Args:
        X (jax.numpy.ndarray): An (S,N) data matrix with data points in rows
        indices (jax.numpy.ndarray): An (S,K) index matrix identifying the values to be picked up from X

    Returns:
        (jax.numpy.ndarray): An (S,K) data matrix subset of X containing K elements from each row of X
    """
    return jnp.take_along_axis(X, indices, axis=1)

def take_along_cols(X, indices):
    """Picks K entries from each column of X specified by indices matrix

    Args:
        X (jax.numpy.ndarray): An (N,S) data matrix with data points in columns
        indices (jax.numpy.ndarray): An (K,S) index matrix identifying the values to be picked up from X

    Returns:
        (jax.numpy.ndarray): An (K,S) data matrix subset of X containing K elements from each column of X
    """
    return jnp.take_along_axis(X, indices, axis=0)

def sparse_approximation(x, K):
    """Keeps only largest K non-zero entries by magnitude in a vector x

    Args:
        x (jax.numpy.ndarray): An data vector/point
        K (int): The number of largest entries to be kept in x

    Returns:
        (jax.numpy.ndarray): x modified so that all entries except the K largest entries are set to 0
    """
    if K == 0:
        return x.at[:].set(0)
    indices = jnp.argsort(jnp.abs(x))
    #print(x, K, indices)
    return x.at[indices[:-K]].set(0)
    
def sparse_approximation_cw(X, K):
    #return jax.vmap(sparse_approximation, in_axes=(1, None), out_axes=1)(X, K)
    """Keeps only largest K non-zero entries by magnitude in each column of X

    Args:
        X (jax.numpy.ndarray): An (N,S) data matrix with data points in columns
        K (int): The number of largest entries to be kept in each column of X

    Returns:
        (jax.numpy.ndarray): X modified so that all entries except the K largest entries are set to 0 in each column
    """
    if K == 0:
        return X.at[:].set(0)
    indices = jnp.argsort(jnp.abs(X), axis=0)
    for c in range(X.shape[1]):
        ind = indices[:-K, c]
        X = X.at[ind, c].set(0)
    return X

def sparse_approximation_rw(X, K):
    """Keeps only largest K non-zero entries by magnitude in each row of X

    Args:
        X (jax.numpy.ndarray): An (S,N) data matrix with data points in rows
        K (int): The number of largest entries to be kept in each row of X

    Returns:
        (jax.numpy.ndarray): X modified so that all entries except the K largest entries are set to 0 in each row
    """
    if K == 0:
        return X.at[:].set(0)
    indices = jnp.argsort(jnp.abs(X), axis=1)
    for r in range(X.shape[0]):
        ind = indices[r, :-K]
        X = X.at[r, ind].set(0)
    return X


def build_signal_from_indices_and_values(length, indices, values):
    """Builds a sparse signal from its non-zero entries (specified by their indices and values)

    Args:
        length (int): Length of the sparse signal
        indices (jax.numpy.ndarray): An index vector of length K identifying non-zero entries
        values (jax.numpy.ndarray): Values to be stored in the non-zero positions

    Returns:
        (jax.numpy.ndarray): Resulting sparse signal such that x[indices] == values 
    """
    x = jnp.zeros(length)
    indices = jnp.asarray(indices)
    values = jnp.asarray(values)
    return x.at[indices].set(values)


def nonzero_values(x):
    """Returns the values of non-zero entries in x

    Args:
        x (jax.numpy.ndarray): A sparse signal

    Returns:
        (jax.numpy.ndarray): The signal stripped of its zero values


    Note:
        This function cannot be JIT compiled as the size of output is data dependent.
    """
    return x[x != 0]

def nonzero_indices(x):
    """Returns the indices of non-zero entries in x

    Args:
        x (jax.numpy.ndarray): A sparse signal

    Returns:
        (jax.numpy.ndarray): The indices of nonzero entries in x

    Note:
        This function cannot be JIT compiled as the size of output is data dependent.

    See Also:
        :func:`support`
    """
    return jnp.nonzero(x)[0]


def support(x):
    """Returns the indices of non-zero entries in x

    Args:
        x (jax.numpy.ndarray): A sparse signal

    Returns:
        (jax.numpy.ndarray): The support of x a.k.a. the indices of nonzero entries in x
        
    Note:
        This function cannot be JIT compiled as the size of output is data dependent.

    See Also:
        :func:`nonzero_indices`
    """
    return jnp.nonzero(x)[0]


def hard_threshold(x, K):
    """Returns the indices and corresponding values of largest K non-zero entries in a vector x

    Args:
        x (jax.numpy.ndarray): A sparse/compressible signal
        K (int): The number of largest entries to be kept in x

    Returns:
        (jax.numpy.ndarray, jax.numpy.ndarray): A tuple comprising of:
            * The indices of K largest entries in x
            * Corresponding entries in x

    See Also:
        :func:`hard_threshold_sorted`
        :func:`hard_threshold_by`
    """
    indices = jnp.argsort(jnp.abs(x))
    I = indices[:-K-1:-1]
    x_I = x[I]
    return I, x_I

def hard_threshold_sorted(x, K):
    """Returns the sorted indices and corresponding values of largest K non-zero entries in a vector x

    Args:
        x (jax.numpy.ndarray): A sparse/compressible signal
        K (int): The number of largest entries to be kept in x

    Returns:
        (jax.numpy.ndarray, jax.numpy.ndarray): A tuple comprising of:
            * The indices of K largest entries in x sorted in ascending order
            * Corresponding entries in x

    See Also:
        :func:`hard_threshold`
    """
    # Sort entries in x by their magnitude
    indices = jnp.argsort(jnp.abs(x))
    # Pick the indices of K-largest (magnitude) entries in x (from behind)
    I = indices[:-K-1:-1]
    # Make sure that indices are sorted in ascending order
    I = jnp.sort(I)
    # Pick corresponding values
    x_I = x[I]
    return I, x_I

def hard_threshold_by(x, t):
    """
    Sets all entries in x to be zero which are less than t in magnitude

    Args:
        x (jax.numpy.ndarray): A sparse/compressible signal
        t (float): The threshold value

    Returns:
        (jax.numpy.ndarray): x modified such that all values below t are set to 0

    Note:
        This function doesn't change the length of x and can be JIT compiled

    See Also:
        :func:`hard_threshold`
    """
    valid = jnp.abs(x) >= t
    return x * valid

def largest_indices_by(x, t):
    """
    Returns the locations of all entries in x which are larger than t in magnitude

    Args:
        x (jax.numpy.ndarray): A sparse/compressible signal
        t (float): The threshold value

    Returns:
        (jax.numpy.ndarray): An index vector of all entries in x which are above the threshold

    Note:
        This function cannot be JIT compiled as the length of output is data dependent

    See Also:
        :func:`hard_threshold_by`
    """
    return jnp.where(jnp.abs(x) >= t)[0]

def dynamic_range(x):
    """Returns the ratio of largest and smallest values (by magnitude) in x (dB)

    Args:
        x (jax.numpy.ndarray): A signal

    Returns:
        (float): The dynamic range between largest and smallest value

    Note:
        This function is not suitable for sparse signals where some values are actually 0

    See Also:
        :func:`nonzero_dynamic_range`
    """
    x = jnp.sort(jnp.abs(x))
    return 20 * jnp.log10(x[-1] / x[0])


def nonzero_dynamic_range(x):
    """Returns the ratio of largest and smallest non-zero values (by magnitude) in x (dB)

    Args:
        x (jax.numpy.ndarray): A sparse/compressible signal

    Returns:
        (float): The dynamic range between largest and smallest nonzero value

    Note:
        This function cannot be JIT compiled as it depends on arrays whose size is data-dependent.

    See Also:
        :func:`dynamic_range`
    """
    x = nonzero_values(x)
    return dynamic_range(x)


def normalize(data, axis=-1):
    """Normalizes a data vector (data - mu) / sigma 

    Args:
        data (jax.numpy.ndarray): A data vector or array
        axis (int): For nd arrays, the axis along which the data normalization will be done

    Returns:
        (jax.numpy.ndarray): Normalized data vector/array
    """
    mu = jnp.mean(data, axis)
    data = data - mu
    variance = jnp.var(data, axis)
    data = data / jnp.sqrt(variance)
    return data

normalize_jit = jit(normalize, static_argnums=(1,))


def frequency_spectrum(x, dt=1.):
    """Frequency spectrum of 1D data using FFT
    """
    n = len(x)
    nn = next_pow_of_2(n)
    X = jfft.fft(x, nn)
    f = jfft.fftfreq(nn, d=dt)
    X = jfft.fftshift(X)
    f = jfft.fftshift(f)
    return f, X

def power_spectrum(x, dt=1.):
    """Power spectrum of 1D data using FFT
    """
    n = len(x)
    T = dt * n
    f, X = frequency_spectrum(x, dt)
    nn = len(f)
    n2 = nn // 2
    f = f[n2:]
    X = X[n2:]
    sxx = (X * jnp.conj(X)) / T
    sxx = jnp.abs(sxx)
    return f, sxx

def energy(data, axis=-1):
    """
    Computes the energy of the signal along the specified axis
    """
    power = jnp.abs(data) ** 2
    return jnp.sum(power, axis)


def interpft(x, N):
    """Interpolates x to n points in Fourier Transform domain
    """
    n = len(x)
    assert n < N
    a = jfft.fft(x)
    nyqst = (n + 1) // 2
    z = jnp.zeros(N -n)
    a1 = a[:nyqst+1]
    a2 = a[nyqst+1:]
    b = jnp.concatenate((a1, z, a2))
    if n % 2 == 0:
        b = b.at[nyqst].set(b[nyqst] /2 )
        b = b.at[nyqst + N -n].set(b[nyqst])
    y = jfft.ifft(b)
    if jnp.isrealobj(x):
        y = jnp.real(y)
    # scale it up
    y = y * (N / n)
    return y


def vec_convolve(x, h):
    """1D full convolution based on a hack suggested by Jake Vanderplas

    See https://github.com/google/jax/discussions/7961 for details
    """
    return signal.convolve(x[None], h[None])[0]

vec_convolve_jit = jit(vec_convolve)

