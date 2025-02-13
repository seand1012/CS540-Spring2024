from scipy.linalg import eigh
import numpy as np
import matplotlib.pyplot as plt


def main():
    x = load_and_center_dataset('Iris_64x64.npy')
    S = get_covariance(x)
    Lambda, U = get_eig_prop(S,0.07)
    print(Lambda)
    print()
    print(U)
    projection = project_image(x[50], U)
    fig, ax1, ax2 = display_image(x[50], projection)
    #plt.show()

'''
Load the dataset from the provided .npy file, 
Center it around the origin, 
Return it as a numpy array of floats
'''
def load_and_center_dataset(filename):
    x = np.load(filename)
    mean = np.mean(x, axis=0)
    x = x - mean
    return x
    
'''
Calculate and return the covariance matrix 
of the dataset as a numpy matrix (d x d array)
'''
def get_covariance(dataset):
    x = np.array(dataset)
    return np.dot(np.transpose(x), x)/420
    

'''
Perform eigendecomposition on the covariance matrix S 
and return a diagonal matrix (numpy array) with the largest 
eigenvalues on the diagonal in descending order, 
and a matrix (numpy array) with the corresponding eigenvectors as columns
'''
def get_eig(S, m):
    # S is covariance matrix
    eigvals, eigvecs = eigh(S)
    sorted_indices = np.argsort(eigvals)[::-1][:m]
    Lambda = np.diag(eigvals[sorted_indices])
    U = eigvecs[:, sorted_indices]
    return Lambda, U

'''
Similar to get_eig, but instead of returning the first m,
return all eigen-values and corresponding eigenvectors in a similar format
that explain more than a prop proproportion of the variance 
(specifically, please make sure the eigenvalues are returned in descending order)
'''
def get_eig_prop(S, prop):
    # Your implementation goes here!
    eigvals, eigvecs = eigh(S)
    sorted_indices = np.argsort(eigvals)[::-1]
    
    total_variance = np.sum(eigvals)
    cumulative_variance = np.sum(eigvals[sorted_indices]) / total_variance
    num_eigvals_to_include = np.argmax(cumulative_variance >= prop) + 1
    #print("sorted indices:", sorted_indices)
    
    Lambda = np.diag(eigvals[sorted_indices[:num_eigvals_to_include]])
    U = eigvecs[:, sorted_indices[:num_eigvals_to_include]]
    return Lambda, U

'''
Project each d x 1 image into your m-dimensional subspace (spanned by
m vectors of size d x 1) and return the new representation as a d x 1 numpy array.
'''
def project_image(image, U):
    flat_image = image.flatten()
    weights = np.dot(np.transpose(U), flat_image)
    projected_image = np.dot(U, weights)
    return projected_image

'''
Use matplotlib to display a visual representation of the original image
and the projected image side-by-side
'''
def display_image(orig, proj):
    orig = orig.reshape(64,64)
    proj = proj.reshape(64,64)
    # Please use the format below to ensure grading consistency
    fig, (ax1, ax2) = plt.subplots(figsize=(9,3), ncols=2)
    ax1.set_title("Original")
    ax2.set_title("Projection")
    orig_pos = ax1.imshow(orig, aspect = 'equal')
    proj_pos = ax2.imshow(proj, aspect = 'equal')
    #pos_orig = plt.imshow(orig, aspect = 'equal')
    #pos_proj = plt.imshow(proj, aspect = 'equal')
    fig.colorbar(orig_pos, ax=ax1)
    fig.colorbar(proj_pos, ax=ax2)
    return fig, ax1, ax2


if __name__ == "__main__":
    main()