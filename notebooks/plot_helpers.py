import numpy as np
import matplotlib.pyplot as plt

from matplotlib.gridspec import GridSpec
from scipy.stats import ks_2samp

def _base_plot(
    v1: np.ndarray,
    v2: np.ndarray,
    nbins: int,
    xlabel:str,
    ylabel: str,
    figname=""
):

    nmax = max(v1.max(), v2.max())
    test = ks_2samp(v1, v2)

    fig = plt.figure(figsize=(6, 6))
    gs = GridSpec(
        2, 2, height_ratios=(4,1), width_ratios=(1,4),
        wspace=0.05, hspace=0.05
    )
    
    ax0 = fig.add_subplot(gs[0, 1])
    ax1 = fig.add_subplot(gs[1, 1])
    ax2 = fig.add_subplot(gs[0, 0])
    
    ax0.scatter(v1, v2, alpha=0.2)
    ax0.plot([1, 1000], [1, 1000])
    ax0.loglog()
    ax0.set_xlim(1, nmax)
    ax0.set_ylim(1, nmax)
    ax0.set_title(f"p={test.pvalue}")
    ax0.set_xticklabels([])
    ax0.set_yticklabels([])
    
    bins = np.logspace(0, np.log10(nmax), nbins)
    cents = (bins[1:] + bins[:-1]) / 2
    
    h, _ = np.histogram(v1, bins=bins)
    
    ax1.step(cents, h, where="mid")
    ax1.set_xlabel(xlabel)
    ax1.semilogx()
    ax1.set_xlim(1, nmax)
    
    h, _ = np.histogram(v2, bins=bins)
    
    ax2.step(h, cents, where="mid")
    ax2.semilogy()
    ax2.set_ylabel(ylabel)
    ax2.set_ylim(1, nmax)

    if figname:
        plt.savefig(figname)
    
    plt.show()

def plot_nmodules(
    nmodules1,
    nmodules2,
    nbins: int=10,
    xlabel=r"$N_{\mathrm{mod}}^{1}$",
    ylabel=r"$N_{\mathrm{mod}}^{2}$",
    figname=""
):
    _base_plot(nmodules1, nmodules2, nbins, xlabel, ylabel, figname=figname)
    
def plot_nmcpe(
    nmcpe1,
    nmcpe2,
    nbins: int=20,
    xlabel=r"$N_{\mathrm{MCPE}}^{1}$",
    ylabel=r"$N_{\mathrm{MCPE}}^{2}$",
    figname=""
):
    _base_plot(nmcpe1, nmcpe2, nbins, xlabel, ylabel, figname=figname)

def _base_histogram_with_ratio(
    v1: np.ndarray,
    v2: np.ndarray,
    nbins: int,
    xlabel: str
):
    bins = np.logspace(0, np.log10(max(v1.max(), v2.max())), nbins)
    cents = (bins[1:] + bins[:-1]) / 2
    widths = bins[1:] - bins[:-1]
    h1, _ = np.histogram(v1, bins=bins)
    h2, _ = np.histogram(v2, bins=bins)

    fig = plt.figure(figsize=(6, 6))
    gs = GridSpec(
        2, 1, height_ratios=(4,1),
        wspace=0.05, hspace=0.05
    )
    
    ax0 = fig.add_subplot(gs[0])
    ax1 = fig.add_subplot(gs[1])
    
    ax0.step(cents, h1 / h2.sum() / widths, where="mid", label="File1", color="crimson")
    ax0.step(cents, h2 / h2.sum() / widths, where="mid", label="File2", color="dodgerblue")

    ax1.step(cents, h1 / h2, where="mid")

    # Configure x-axes
    ax0.semilogx()
    ax1.semilogx()
    ax0.set_xticklabels([])
    ax0.set_xlim(1, bins.max())
    ax1.set_xlim(1, bins.max())
    ax1.set_xlabel(xlabel)

    # Configure y-axes
    ax0.set_ylabel("PDF")
    ax1.set_ylabel("File1/File2")

    # Configure legend
    ax0.legend()

    plt.show()

def nmcpe_histogram_ratio(v1, v2, nbins=20, xlabel=r"$N_{\mathrm{MCPE}}$"):
    _base_histogram_with_ratio(v1, v2, nbins=nbins, xlabel=xlabel)

def nmodule_histogram_ratio(v1, v2, nbins=10, xlabel=r"$N_{\mathrm{mod}}$"):
    _base_histogram_with_ratio(v1, v2, nbins=nbins, xlabel=xlabel)
