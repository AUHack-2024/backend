import jax.numpy as jnp
import jax.scipy as jsp
from PIL import Image
import jax


def to_grayscale(img):
    '''Converts an RGBA image to grayscale'''
    return jnp.mean(img, axis=2)

def normalize_lumincance(img):
    '''Normalizes the luminance values of an image so that the min value is 0 and the max value is 255'''
    image = img.astype(jnp.float32) 
    normalized = (image - jnp.min(image)) / (jnp.max(image) - jnp.min(image))
    normalized = normalized * 255
    return normalized.astype(jnp.uint8)

def resize_square(img, side_length):
    '''Resizes an image to a square with the specified side length'''
    return jax.image.resize(img, (side_length, side_length), method='bilinear')


def get_tiles(img, subdiv=5):
    '''Splits an image into a grid of tiles'''
    tile_size = img.shape[0] // subdiv
    
    def slice_tile(i, j):
        start_indices = jnp.array([i * tile_size, j * tile_size])
        slice_sizes = jnp.array([tile_size, tile_size])
        return jax.lax.dynamic_slice(img, start_indices, slice_sizes)
    
    def generate_indices(subdiv):
        '''Helper function to generate all possible indices for the tiles'''
        i_indices = jnp.repeat(jnp.arange(subdiv), subdiv)
        j_indices = jnp.tile(jnp.arange(subdiv), subdiv)
        return jnp.stack((i_indices, j_indices), axis=-1)
    indices = generate_indices(subdiv)
    tiles = jax.vmap(lambda idx: slice_tile(idx[0], idx[1]))(indices)
    
    return jnp.stack(tiles)

def ssim(img_1, img_2, subdiv=10):
    def get_ssim_tile(img_1, img_2):
        mu_x = jnp.mean(img_1)
        mu_y = jnp.mean(img_2)
        sigma_x = jnp.std(img_1)
        sigma_y = jnp.std(img_2)
        sigma_xy = jnp.mean((img_1 - mu_x) * (img_2 - mu_y))
        
        c1 = 0.01
        c2 = 0.03
        
        ssim = (2 * mu_x * mu_y + c1) * (2 * sigma_xy + c2) / ((mu_x**2 + mu_y**2 + c1) * (sigma_x**2 + sigma_y**2 + c2))
        return ssim
    
    tiles_1 = get_tiles(img_1, subdiv)
    tiles_2 = get_tiles(img_2, subdiv)
    
    ssim_values = jax.vmap(get_ssim_tile)(tiles_1, tiles_2)
    
    return jnp.mean(ssim_values)


def blur(img, window=50):
    x = jnp.linspace(-3, 3, window)
    window = jsp.stats.norm.pdf(x) * jsp.stats.norm.pdf(x[:, None])
    window = window / jnp.sum(window, keepdims=True)
    
    return jsp.signal.convolve2d(img, window, mode='same')

    

def mse(img_1, img_2):
    blur_img_1 = blur(img_1, 50)
    blur_img_2 = blur(img_2, 50)
    return jnp.mean((blur_img_1 - blur_img_2)**2)


def norm_mse(z, slope=80):
    return 1/(z/slope + 1)


def get_scores(frame1, frame2, w1=0.8, w2=0.2):
    assert w1 + w2 == 1, "Weights must sum to 1"
    f1 = resize_square(normalize_lumincance(to_grayscale(frame1)))
    f2 = resize_square(normalize_lumincance(to_grayscale(frame2)))

    ssim_score = ssim(f1, f2)
    mse_score = mse(f1, f2)
    norm_mse_score = norm_mse(mse_score)
    return w1 * ssim_score + w2 * norm_mse_score