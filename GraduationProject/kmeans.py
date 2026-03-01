from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import matplotlib
import matplotlib.pyplot as plt


def restore_image(cb, cluster, shape):
    row, col, dummy = shape
    image = np.empty((row, col, dummy))
    for r in range(row):
        for c in range(col):
            image[r, c] = cb[cluster[r * col + c]]
    return image


def show_scatter(a):
    N = 10
    density, edges = np.histogramdd(a,
                                    bins=[N, N, N],
                                    range=[(0, 1), (0, 1), (0, 1)])
    density /= density.max()
    x = y = z = np.arange(N)
    d = np.meshgrid(x, y, z)

    fig = plt.figure(1, facecolor='w')
    ax = fig.add_subplot(111, projection='3d')

    cm = matplotlib.colors.ListedColormap(list('rgbm'))
    ax.scatter(d[0],
               d[1],
               d[2],
               s=100 * density,
               cmap=cm,
               marker='o',
               depthshade=True)
    ax.set_xlabel(u'红')
    ax.set_ylabel(u'绿')
    ax.set_zlabel(u'蓝')
    plt.title(u'图像颜色三维频数分布', fontsize=20)

    plt.figure(2, facecolor='w')
    den = density[density > 0]
    den = np.sort(den)[::-1]
    t = np.arange(len(den))
    plt.plot(t, den, 'r-', t, den, 'go', lw=2)
    plt.title(u'图像颜色频数分布', fontsize=18)
    plt.grid(True)

    plt.show()


if __name__ == '__main__':
    matplotlib.rcParams['font.sans-serif'] = [u'SimHei']
    matplotlib.rcParams['axes.unicode_minus'] = False
    # 聚类数2,6,30
    num_vq = 2
    im = Image.open('static/1.jpg')
    image = np.array(im).astype(np.float) / 255
    image = image[:, :, :3]
    image_v = image.reshape((-1, 3))
    kmeans = KMeans(n_clusters=num_vq, init='k-means++')
    #show_scatter(image_v)

    N = image_v.shape[0]  # 图像像素总数
    # 选择样本，计算聚类中心
    idx = np.random.randint(0, N, size=int(N * 0.7))
    image_sample = image_v[idx]
    kmeans.fit(image_sample)
    result = kmeans.predict(image_v)  # 聚类结果
    print('聚类结果:\n', result)
    print('聚类中心:\n', kmeans.cluster_centers_)

    vq_image = restore_image(kmeans.cluster_centers_, result, image.shape)
    plt.axis('off')
    plt.title(u'聚类个数:%d' % num_vq, fontsize=20)
    plt.imshow(vq_image)
    # plt.savefig('矢量化图片.png')

    plt.tight_layout(1.2)
    plt.show()