# IPython log file


from skimage import io
spacing = [3.033534 * 3, 3.033534, 3.033534]
skel1 = io.imread('OP_1_Rendered_Paths_thinned.tif')
from skan import csr
df = csr.summarise(skel1.astype(bool), spacing=spacing)
df2 = pd.read_excel('OP_1-Branch-information.xlsx')
bins = np.histogram(np.concatenate((df['branch-distance'],
                                    df2['Branch length'])),
                    bins=35)[1]
plt.hist(df['branch-distance'], bins=bins, label='skan');
plt.hist(df2['Branch length'], bins=bins, label='Fiji', alpha=0.3);
plt.legend()
plt.xlabel('Branch length (µm)')
plt.ylabel('Count')
plt.title('OP1 Branch lengths')
plt.savefig('OP1 Branch lengths using skan and Fiji.png')
